import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import Formula, FloatVector
import rpy2.robjects.packages as rpackages

import re


def _install_rpackage(pkg_name: str):
    if not rpackages.isinstalled(pkg_name):
        # Import the utils package to use for installation
        utils = rpackages.importr('utils')
        # Set a CRAN mirror
        utils.chooseCRANmirror(ind=1)
        # Install the package
        utils.install_packages(pkg_name)
        print(f"Package '{pkg_name}' installed successfully.")


def get_stars(p_value):
    if p_value > .05:
        return 'ns'
    elif .01 < p_value <= .05:
        return '*'
    elif .001 < p_value < .01:
        return '**'
    elif .0001 < p_value < .001:
        return '***'
    elif p_value < .0001:
        return '****'
    else:
        return False, f'error in determining stars for p_value {p_value}'


def r_mannwhitneyu_test(groupA, groupB, print_result=False):
    return r_wilcoxsign_test(groupA, groupB, print_result=print_result, __paired_groups=False)


def r_wilcoxsign_test(groupA, groupB, print_result=False, __paired_groups=True):
    # Install and import R packages
    _install_rpackage('coin')

    coin = importr('coin')
    base = importr('base')

    GroupA = FloatVector(groupA)
    GroupB = FloatVector(groupB)

    # Test1 using base R's wilcox.test
    test_result1 = ro.r['wilcox.test'](GroupA, GroupB, paired=__paired_groups)
    test_result1_str = str(test_result1)

    if print_result:
        print("Test1 Result:")
        print(test_result1_str)

    # Regex pattern for Test1 to extract V (W) statistic
    if __paired_groups:
        pattern_test1 = r"V\s*=\s*(\d+\.?\d*),\s*p-value\s*(=|<)\s*([\d\.]+([eE][+-]?\d+)?|\d+\.?\d*)"
    else:
        pattern_test1 = pattern_test1 = r"W\s*=\s*(\d+\.?\d*),\s*p-value\s*(=|<)\s*([\d\.]+([eE][+-]?\d+)?|\d+\.?\d*)"

    match_test1 = re.search(pattern_test1, test_result1_str)

    if match_test1:
        v_or_w_value = float(match_test1.group(1))
        p_value1 = float(match_test1.group(3))

    # Test2 using coin package

    if __paired_groups:
        # Combine the two groups into an R data frame
        data = base.data_frame(GroupA=GroupA, GroupB=GroupB)

        # Define the formula for the test
        formula = Formula('GroupA ~ GroupB')

        # Perform the Wilcoxon signed-rank test using the wilcoxsign_test function
        test_result2 = coin.wilcoxsign_test(formula, data=data, distribution="exact", alternative="two.sided")
    else:
        # via https://yatani.jp/teaching/doku.php?id=hcistats:mannwhitney
        # Implementing the requested non-paired version
        # Create the group factor and combined value vector
        g = base.factor(base.c(base.rep("GroupA", len(GroupA)), base.rep("GroupB", len(GroupB))))
        v = base.c(GroupA, GroupB)

        # Create a data frame combining the groups and values
        data = base.data_frame(Value=v, Group=g)

        # Define the formula for the test
        formula = Formula('Value ~ Group')

        # Perform the Wilcoxon rank-sum test using the wilcox_test function
        test_result2 = coin.wilcox_test(formula, data=data, distribution="exact", alternative="two.sided")
    test_result2_str = str(test_result2)

    if print_result:
        print("Test2 Result:")
        print(test_result2_str)

    # Regex pattern for Test2 to extract Z and p-value
    pattern_test2 = r"Z\s*=\s*(-?\d+\.\d+),\s*p-value\s*(=|<)\s*([\d\.]+([eE][+-]?\d+)?|\d+\.?\d*)"
    match_test2 = re.search(pattern_test2, test_result2_str)

    if match_test2:
        z_value = float(match_test2.group(1))
        p_value2 = float(match_test2.group(3))
    else:
        z_value, p_value2 = None, None

    r_value = abs(z_value / (len(GroupA) + len(GroupB)) ** .5) if z_value is not None else None

    effect_size = ""

    p_value = max([p_value1, p_value2])

    if p_value < .05:
        effect_size = f", r = {r_value}"
    report = f"{'W' if __paired_groups else 'U'} = {v_or_w_value}, Z = {z_value}, p = {p_value}{effect_size}"

    w_or_u_key = "w_statistics" if __paired_groups else "u_statistics"

    return {w_or_u_key: v_or_w_value, 'z_statistics': z_value, 'p_value': p_value,
            'r_value': round(r_value, 5) if r_value is not None else None,
            'report': report}


def R_art_rmanova(df, indep_vars: list, response_var: str, subject_id_var: str, formula=None, print_anova=True,
                  print_latex_report=True):
    """Rpy2 binding for ART ANOVA in Python. Version 2. Written by Jonathan Liebers on 2025-01-21."""
    import pandas as pd
    from datetime import datetime
    from rpy2.robjects import r, pandas2ri, Formula
    import rpy2.robjects as ro
    import rpy2.robjects.conversion as conversion
    from rpy2.robjects.packages import importr
    from itertools import combinations
    import string
    try:
        import rpy2.ipython.html
        rpy2.ipython.html.init_printing()
    except:
        pass  # no jupyter environment

    def significance_level(p):
        if p < 0.0001:
            return '****'
        elif p < 0.001:
            return '***'
        elif p < 0.01:
            return '**'
        elif p < 0.05:
            return '*'
        elif p < 0.1:
            return '.'
        else:
            return ''

    def anova_effect_sizes(eta_square):
        if eta_square >= 0.14:
            return "large"
        elif eta_square >= 0.06:
            return "medium"
        elif eta_square >= 0.01:
            return "small"
        else:
            return ""

    def rmanova_latex_report(anova, posthocs, factors, dep_var, df, round_to_float=4):
        def ff(val, fmt="%.4f"):  # format float
            ret = fmt % val
            if ret.startswith("0."):
                return ret[1:]
            if ret.startswith("-0."):
                return "-" + ret[2:]
            return ret

        def desc_formatter(row):
            try:
                return f"\\newcommand{{\\{''.join(row.name)}DescStats}}{{Med.~=~{ff(row['median'], '%.2f')}, IQR~=~{ff(row['iqr'], '%.2f')}}}"
            except:
                return f"\\newcommand{{\\{row.name}DescStats}}{{Med.~=~{ff(row['median'], '%.2f')}, IQR~=~{ff(row['iqr'], '%.2f')}}}"

        def calculate_desc_stats(df, grouping_terms):
            grouped = df.groupby(grouping_terms)[dep_var]
            median = grouped.median()
            iqr = grouped.quantile(0.75) - grouped.quantile(0.25)

            desc_df = pd.DataFrame({
                'median': median,
                'iqr': iqr
            })

            desc_df['latex'] = desc_df.apply(desc_formatter, axis=1)
            return desc_df

        def anova_reporter(row):
            if 'Term' in row.keys():
                return f'F({int(row["Df"])},~{int(row["Df.res"])})~=~{ff(row["F value"])}, p~=~{ff(row["Pr(>F)"])}, \\etasqp~=~{ff(row["eta.sq.part"])}'.replace(
                    "p~=~.0000", "p < .0001")
            else:  # Contrast
                return f't({int(row["df"])})~=~{ff(row["t.ratio"])}, p~=~{ff(row["p.value"])}'.replace("p~=~.0000",
                                                                                                           "p~<~.0001")

        def anova_latex_reporter(row):
            if 'Term' in row.keys():
                # Handle main effects and interaction effects
                effect_type = "MainEffect" if ":" not in row.Term else "InteractionEffect"
                term_cleaned = str(row.Term).replace(":", "")
                return (
                    "\\newcommand{\\anova" + effect_type + term_cleaned + "}{"
                    + anova_reporter(row) + "}  %" + row.name
                )
            else:  # Handle contrasts
                contrast_cleaned = str(row.contrast).replace(" - ", "xxxVSxxx").replace(',', '')
                contrast_report = anova_reporter(row)
                contrast_np_report = contrast_report[1:-1]
                return (
                    "\\newcommand{\\Contrast" + contrast_cleaned + "}{"
                    + contrast_report + "}  %" + row.name #+ '\n' +
                    #"\\newcommand{\\Contrast" + contrast_cleaned + "NP}{"
                    #+ contrast_np_report + "}  %" + row.name + '\n'
                )

        def print_anova(anova, posthocs, round_to_float):
            r = round_to_float
            anova['report'] = anova.round(r).apply(anova_reporter, axis=1)
            anova['latex'] = anova.round(r).apply(anova_latex_reporter, axis=1)
            print()
            print("% --- RM-ANOVA REPORT (WITHIN SUBJECT WITH EQUAL GROUP SIZES) ---")
            print("% Report generated on", datetime.now().strftime("# %Y-%m-%d %H:%M:%S"))
            print("\\newcommand{\\etasqp}{$\\eta^2_{p}$}")
            print("\\begin{comment}")
            print('ANOVA')
            print(anova.round(r).to_markdown())
            print("\\end{comment}")
            for l in anova.round(r).latex.unique():
                l = str(l)
                if len(l) > 1:
                    print(l)

            for key in posthocs.keys():
                print()
                posthoc = posthocs[key]
                posthoc['report'] = posthoc.round(r).apply(anova_reporter, axis=1)
                posthoc['latex'] = posthoc.round(r).apply(anova_latex_reporter, axis=1)
                print("\\begin{comment}")
                print(key)
                print(posthoc.round(r).to_markdown())
                print("\\end{comment}")
                for l in posthoc.round(r).latex.unique():
                    l = str(l)
                    if len(l) > 1:
                        print(l)

        # Print ANOVA and post-hoc analyses if provided
        if anova is not None and posthocs is not None:
            print_anova(anova, posthocs, round_to_float)

        print("% DESCRIPTIVES")
        # Iterate through all combinations of factors
        for r in range(1, len(factors) + 1):  # r is the size of the combination
            for group_combination in combinations(factors, r):
                if len(group_combination) == 1:
                    group_combination2 = group_combination[0]
                else:
                    group_combination2 = list(group_combination)
                desc_stats = calculate_desc_stats(df, group_combination2)
                for row in desc_stats.latex.unique():
                    print(row)

    # Import necessary R packages
    artool = importr('ARTool')
    rcpp = importr('Rcpp')
    dplyr = importr('dplyr')

    # Activate pandas-to-R dataframe conversion
    pandas2ri.activate()

    rdf = conversion.py2rpy(df)

    # Prepare data for R dataframe
    data_dict = {factor: r['as.factor'](rdf.rx2[factor]) for factor in indep_vars}
    data_dict[response_var] = rdf.rx2[response_var]
    data_dict[subject_id_var] = r['as.factor'](rdf.rx2[subject_id_var])

    rdf = r['data.frame'](**data_dict)

    # If formula is not provided, construct a default one
    if formula is None:
        independent_vars = " * ".join(indep_vars)
        formula = f"{response_var} ~ {independent_vars} + Error({subject_id_var})"

    # R execution stuff
    m_art = r.art(Formula(formula), data=rdf)
    r.assign("m_art", m_art)

    anova_result = r.anova(m_art)
    r.assign("anova_result", anova_result)

    # Calculate partial eta square
    r("""anova_result$eta.sq.part = with(anova_result, `Sum Sq`/(`Sum Sq` + `Sum Sq.res`))""")

    # Convert ANOVA to Python
    with (ro.default_converter + pandas2ri.converter).context():
        anova_result = ro.conversion.get_conversion().rpy2py(r["anova_result"])

    # Add significance and effect size columns
    anova_result['sig.'] = anova_result['Pr(>F)'].apply(lambda x: significance_level(x))
    anova_result['effect_size'] = anova_result['eta.sq.part'].apply(lambda x: anova_effect_sizes(x))

    # Determine posthocs for significant rows
    run_posthoc = anova_result["Term"].tolist()

    posthocs = {}
    if len(run_posthoc) > 0:
        for combo, letter in zip(run_posthoc, string.ascii_lowercase):
            r(f"""posthoc.{letter} <- art.con(m_art, "{combo}", adjust="holm") %>%  \
                                      summary() %>%  \
                                      mutate(sig. = symnum(p.value, corr=FALSE, na=FALSE,
                                      cutpoints = c(0, 0.0001,     0.001, 0.01, 0.05, 0.1, 1),
                                      symbols =   c(   "****",     "***", "**", "*",  ".", " ")))
                                      posthoc.{letter}""")
            with (ro.default_converter + pandas2ri.converter).context():
                posthocs.update({combo: ro.conversion.get_conversion().rpy2py(r[f"posthoc.{letter}"])})

    if print_anova:
        print(f"R ART RM-ANOVA with formula `{formula}`")
        try:
            display(anova_result)
        except:
            print(anova_result)

        for i, key in enumerate(posthocs.keys()):
            print(f"\nPosthoc/contrast test nr. {i + 1} for `{key}`")
            try:
                display(posthocs[key])
            except:
                print(posthocs[key])

    if print_latex_report:
        rmanova_latex_report(anova_result, posthocs, indep_vars, response_var, df)
        print("% --- END OF RM-ANOVA REPORT ---")

    return anova_result, posthocs

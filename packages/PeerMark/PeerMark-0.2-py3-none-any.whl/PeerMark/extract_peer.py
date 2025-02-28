import pandas as pd

def read_command_line():
    from argparse import ArgumentParser as AP
    from canvas_selector import choose_options
    parser = AP()
    parser.add_argument('-c', '--course', help="Canvas courseID",
                        default=None)
    parser.add_argument('-s', '--semester', help='semester id, e.g. "2241"',
                        default=None)

    args = parser.parse_args()
    args.assignment = True
    args.groups = True
    args = choose_options(args)
    args.ass = args.asses[0]
    return args 


def build_group_dict(groups, subs):
    """ given the group set from canvas, and the submissions for this assignment, build a dictionary where each group (key) has the list of submission (value)."""

    group_dict = {}
    for group in groups:
        group_ids = [user.id for user in group.get_users()]
        group_dict[group] = [sub for sub in subs if sub.user_id in group_ids
                             and len(sub.attachments) > 0]
    return group_dict


def download_submissions(args):
    from canvas_selector import get_submissions
    # download the files 
    get_submissions(args.ass, ungraded_only=False) 
    # build the subs list
    subs = args.ass.get_submissions() 
    for sub in subs:
        sub.name = args.course.get_user(sub.user_id).name
    groups = args.group.get_groups()

    return build_group_dict(groups, subs)


def extract_data(fname):
    """given the path to an excel file, pull the data into a dataframe"""
    df = pd.read_excel(fname)
    df.drop_duplicates(subset="NAME:", inplace=True)
    df.set_index("NAME:", inplace=True)
    df = df[df.index.notnull()]
    return df


def writedata(df, subs):
    """given a data frame containing all the collected comments for a given group, pull out the comments for each member, write them to a file, then calculate the mark awarded and update the canvas submission with the mark and comments"""
    import numpy as np
    from canvas_selector import nameFile, update_grade

    for sub in subs:
        fname = nameFile(sub)
        df_ = df[sub.name].copy()
        df_.columns = ['' for _ in range(len(df_.columns))]

        df_.to_excel(fname)
        mark = np.round(10*np.average(df_.iloc[[len(df_)-1]]),0)
        update_grade(sub, mark)
        sub.upload_comment(fname)


def grade_submissions(args, group_dict):
    """given a dictionary explaining which submissions belongs to which group, collect the marks and comments for the entire team. Then call writedata to update the canvas submissions"""
    import os
    from canvas_selector import nameFile
    from tqdm import tqdm

    for group in tqdm(group_dict, desc=f"Grading     {args.ass.name}", ascii=True):
        fulldf = pd.DataFrame()
        subs = group_dict[group]
        for sub in subs:
            fname = nameFile(sub)
            if os.path.isfile(fname):
                tmpdf = extract_data(fname)
                fulldf = pd.concat([fulldf, tmpdf], axis=1)

        writedata(fulldf, subs)


def main():
    from canvas_selector import cleanup
    args = read_command_line()
    group_dict = download_submissions(args)
    grade_submissions(args, group_dict)
    cleanup(args.ass.assignment_id)


if __name__ == '__main__':
    main()

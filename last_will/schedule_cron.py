from crontab import CronTab
import os
from pathlib import Path
from argparse import ArgumentParser


def cron_job():
    my_cron = CronTab(user=True)

    parser = ArgumentParser(description="Set cron job parameters")
    parser.add_argument('-s', '--shell', help="Set the shell environment. Default is sh.")
    parser.add_argument('-p', '--path', help="Set a custom PATH for cron. Default is \"/usr/bin:/bin\"")
    parser.add_argument('-m', '--mailto',
                        help="Set a local to whom emails are sent by the cron job. "
                             "Set to \"\" to deactivate emails altogether. Default is current user.")
    parser.add_argument('-t', '--time', default='12:00',
                        help="Set the time when the cron job will be run. Default is 12:00")
    parser.add_argument('-d', '--display', action='store_true', help="Display the active configuration and cron jobs")
    parser.add_argument('-r', '--reset', action='store_true', help="Restore configuration and delete cron job")

    args = parser.parse_args()

    if args.shell:
        my_cron.env['SHELL'] = args.shell
    if args.path:
        my_cron.env['PATH'] = args.path
    if args.mailto:
        my_cron.env['MAILTO'] = args.mailto
    if args.display:
        os.system('crontab -l')
    elif args.reset:
        os.system('crontab -r')
        os.system('crontab -l')
    else:
        my_cron.remove_all(comment='check in')
        job = my_cron.new(command=f'cd {Path.cwd()} && python3 check_in.py', comment='check in')
        job.day.every(1)
        job.hour.on(args.time.split(':')[0].strip())
        job.minute.on(args.time.split(':')[1].strip())

    my_cron.write()


if __name__ == '__main__':
    cron_job()


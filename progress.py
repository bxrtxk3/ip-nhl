import sys

def percentageProgress(progress, total, message = ''):
    percent = 100 * (progress / total)
    sys.stdout.write("{}Current progress: %d%% ({}/{})".format(message + ' - ' if message != '' else '', progress, total) % (percent))
    sys.stdout.write('\r')
    sys.stdout.flush()

def progressNewLine():
    sys.stdout.write('\n')
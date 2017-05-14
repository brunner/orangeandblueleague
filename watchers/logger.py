import datetime


class Logger(object):
  """Records log entries."""

  def __init__(self, slack=True):
    self.slack = slack

    self.collected = []
    self.logs = []

  def timestamp(self):
    return datetime.datetime.now().strftime('%H:%M:%S')

  def log(self, message):
    t = self.timestamp()
    self.logs.append("[{0}] {1}".format(t, message))

  def collect(self):
    ret = self.logs
    self.collected.extend(self.logs)
    self.logs = []
    return ret


class TestLogger(Logger):
  """Test implementation of Logger."""

  def timestamp(self):
    return "00:00:00"
import datetime
import slack


class Logger(object):
  """Records log entries."""

  def __init__(self, slack=True):
    self.slack = slack

    self.logs = []
    self.queue = []

  def timestamp(self):
    return datetime.datetime.now().strftime('%H:%M:%S')

  def log(self, message):
    t = self.timestamp()
    self.queue.append("[{0}] {1}".format(t, message))

  def dump(self):
    if self.queue and self.slack:
      slack.postMessage("\n".join(self.queue), "testing")
    self.logs.extend(self.queue)
    self.queue = []


class TestLogger(Logger):
  """Test implementation of Logger."""

  def timestamp(self):
    return "0:0:0"
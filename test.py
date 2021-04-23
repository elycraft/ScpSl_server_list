from notifypy import Notify

notification = Notify()
notification.application_name = "SCP:SL Serveurs"
notification.title = "11/25 joueurs sur %s"%"tes"
notification.message = "Even cooler message."

notification.send()
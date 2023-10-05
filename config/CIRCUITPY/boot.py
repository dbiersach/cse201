import usb_cdc
import usb_hid
import usb_midi
import storage

usb_midi.disable()
usb_hid.disable()
storage.disable_usb_drive()
usb_cdc.enable(console=True, data=True)
print("BNL CSE201 OCT 2023")

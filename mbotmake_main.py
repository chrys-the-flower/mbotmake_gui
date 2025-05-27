import wx

#import the newly created GUI file
import mbotmake_gui
import mbotmake
class MBotFrame(mbotmake_gui.MyFrame2):
   def __init__(self,parent):
      mbotmake_gui.MyFrame2.__init__(self,parent)

   def mbotmake_conv(self,event):
      in_file = str(self.m_filePicker_input.GetPath())
      print(in_file)
      slicer = str(self.m_choice_slicer.GetSelection())
      print(slicer)
      printer = str(self.m_choice_printer.GetSelection())
      print(printer)
      extruder = str(self.m_choice_extruder.GetSelection())
      print(extruder)
      is_done = mbotmake.main(in_file, printer, extruder, slicer)
      if is_done:
            self.m_staticText41.SetLabel("Done!")
      else:
         self.m_staticText41.SetLabel("Error, invalid file!")



app = wx.App(False)
frame = MBotFrame(None)
frame.Show(True)
#start the applications
app.MainLoop()
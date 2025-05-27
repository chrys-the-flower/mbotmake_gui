# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"GCode to .makerbot"), pos = wx.DefaultPosition, size = wx.Size( 444,312 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, _(u"Select input .gcode file to convert"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        bSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )

        self.m_filePicker_input = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, _(u"Select a file"), _(u"*.gcode"), wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer1.Add( self.m_filePicker_input, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, _(u"Slicer"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        self.m_staticText4.Hide()

        bSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )

        m_choice_slicerChoices = [ _(u"Prusa"), _(u"Orca") ]
        self.m_choice_slicer = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_slicerChoices, 0 )
        self.m_choice_slicer.SetSelection( 0 )
        self.m_choice_slicer.Hide()

        bSizer1.Add( self.m_choice_slicer, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Printer Type"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        bSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        m_choice_printerChoices = [ _(u"Replicator+"), _(u"Replicator 5"), _(u"Replicator Mini 5"), _(u"Replicator Mini+") ]
        self.m_choice_printer = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_printerChoices, 0 )
        self.m_choice_printer.SetSelection( 0 )
        bSizer1.Add( self.m_choice_printer, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Extruder Type"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        bSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        m_choice_extruderChoices = [ _(u"Smart Extruder+"), _(u"Smart Extruder"), _(u"Tough Extruder"), _(u"Experimental Extruder") ]
        self.m_choice_extruder = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_extruderChoices, 0 )
        self.m_choice_extruder.SetSelection( 0 )
        bSizer1.Add( self.m_choice_extruder, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_button_generate = wx.Button( self, wx.ID_ANY, _(u"Generate .makerbot"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer1.Add( self.m_button_generate, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_gauge3 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.m_gauge3.SetValue( 0 )
        self.m_gauge3.Hide()

        bSizer1.Add( self.m_gauge3, 0, wx.ALL|wx.EXPAND, 5 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText41.Wrap( -1 )

        bSizer2.Add( self.m_staticText41, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button_generate.Bind( wx.EVT_BUTTON, self.mbotmake_conv )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def mbotmake_conv( self, event ):
        event.Skip()



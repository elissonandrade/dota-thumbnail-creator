#! /usr/bin/python

from gimpfu import *
import gtk
import gimpui
import gobject
import os

def choose_directory(widget, combobox, liststore, labelPath):
    dialog = gtk.FileChooserDialog("Select a directory", None, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                   (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                    gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        folder_path = dialog.get_filename()
        labelPath.set_text(folder_path)
        populate_combobox(folder_path, combobox, liststore)
    dialog.destroy()

def populate_combobox(folder_path, combobox, liststore):
    liststore.clear()
    image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    for image_file in image_files:
        liststore.append([image_file])

def preview_gen(widget, image_ref, reactionPath, reactionFile, thumbText, heroPath, heroFile):
    temp_img = pdb.gimp_image_new(
        image_ref.width,
        image_ref.height,
        image_ref.base_type)
    temp_img.disable_undo()
    for layer in image_ref.layers:
        temp_layer = pdb.gimp_layer_new_from_drawable(layer, temp_img)
        temp_img.insert_layer(temp_layer)
        if len(layer.children) == 0: # Cannot add alpha for layer group
            pdb.gimp_layer_add_alpha(temp_layer)
        pdb.gimp_drawable_set_visible(temp_layer, True)
    
    separator = "\\"
    
    pdb.gimp_image_scale(image_ref,1280,720)
    
    pdb.gimp_message(reactionPath.get_text()+ separator +reactionFile.get_active_text())
    reactionLay = pdb.gimp_file_load_layer(image_ref,reactionPath.get_text()+ separator +reactionFile.get_active_text())
    pdb.gimp_message("Opened image")
    pdb.gimp_image_insert_layer(image_ref,reactionLay,None,-1)
    pdb.gimp_layer_scale(reactionLay, 750, 400,FALSE)
    #pdb.gimp_layer_resize(reactionLay, 400, 400,0,0)
    pdb.gimp_item_transform_translate(reactionLay, 0, 320)
    pdb.gimp_message(heroPath.get_text()+ separator + heroFile.get_active_text())
    reactionHero = pdb.gimp_file_load_layer(image_ref,heroPath.get_text()+ separator + heroFile.get_active_text())
    pdb.gimp_image_insert_layer(image_ref,reactionHero,None,-1)
    pdb.gimp_layer_scale(reactionHero, 400, 400,FALSE)
    pdb.gimp_item_transform_translate(reactionHero, 865, 62)
    
    [startB,endB] = thumbText.get_bounds();
    pdb.gimp_message(thumbText.get_text(startB,endB));
    textLay = pdb.gimp_text_fontname(image_ref,None,30.0,30.0,thumbText.get_text(startB,endB),0, TRUE,62,POINTS,pdb.gimp_context_get_font())
    pdb.gimp_text_layer_set_justification(textLay, TEXT_JUSTIFY_CENTER)
    pdb.gimp_text_layer_resize(textLay, 800, 650)
    
    window = gtk.Window()
    window.set_title("Preview")
    display_box = gtk.VBox(spacing=10)
    #if preview_box is not None:
    #    display_box.remove(preview_box)

    preview_box = gimpui.DrawablePreview(temp_img.flatten())
    display_box.pack_start(preview_box, True, True, 0)
    gtk.main_quit()
    #window.show_all()

def gen_thumb(_image, _drawable, _reactionPath, _heroPath, _thumbText):
    window = gtk.Window()
    window.set_title("Generate Video Thumbnail")
    window.connect('destroy',  close_plugin_window)
    window_box = gtk.VBox(spacing=10)

    hbReaction = gtk.HBox(spacing=10)
    lbReactionDir = gtk.Label("Choose Reaction Directory:")
    
    hbReaction.pack_start(lbReactionDir, False, False, 0)
    
    lbReactionPath = gtk.Label(_reactionPath)
    
    hbReaction.pack_start(lbReactionPath, False, False, 0)
    
    btReaction = gtk.Button("Browse...")
    
    hbReaction.pack_start(btReaction, False, False, 0)
    window_box.pack_start(hbReaction, False, False, 0)
    
    hbReaction = gtk.HBox(spacing=10)
    lbReaction = gtk.Label("Choose Reaction File:")
    hbReaction.pack_start(lbReaction, False, False, 0)
    
    cbReaction = gtk.ComboBox()
    lsReaction = gtk.ListStore(str)
    cbReaction.set_model(lsReaction)

    if _reactionPath.strip() != "" :
        populate_combobox(_reactionPath, cbReaction, lsReaction)

    cell = gtk.CellRendererText()
    cbReaction.pack_start(cell, True)
    cbReaction.add_attribute(cell, 'text', 0)

    btReaction.connect("clicked", choose_directory, cbReaction, lsReaction, lbReactionPath)
    hbReaction.pack_start(cbReaction, False, False, 0)
    
    window_box.pack_start(hbReaction, False, False, 0)
    
    # Multiline text input
    hbText = gtk.HBox(spacing=10)
    lbText = gtk.Label("Enter Thumbnail Text:")
    hbText.pack_start(lbText, False, False, 0)

    txtview = gtk.TextView()
    textbuffer = txtview.get_buffer()
    if not _thumbText:
        textbuffer.set_text("Enter the text that will be centered on the thumbnail here")
    else:
        textbuffer.set_text(_thumbText)
    hbText.pack_start(txtview, True, True, 0)

    window_box.pack_start(hbText, True, True, 0)
    
    hbHeroDir = gtk.HBox(spacing=10)
    lbHeroesDir = gtk.Label("Choose Heroes Directory:")
    
    hbHeroDir.pack_start(lbHeroesDir, False, False, 0)
    
    lbHeroPath = gtk.Label(_heroPath)
    
    hbHeroDir.pack_start(lbHeroPath, False, False, 0)
    
    btHeroes = gtk.Button("Browse...")
    
    hbHeroDir.pack_start(btHeroes, False, False, 0)
    window_box.pack_start(hbHeroDir, False, False, 0)
    
    hbHeroes = gtk.HBox(spacing=10)
    lbHeroes = gtk.Label("Choose Hero File:")
    hbHeroes.pack_start(lbHeroes, False, False, 0)
    
    cbHeroes = gtk.ComboBox()
    lsHeroes = gtk.ListStore(str)
    cbHeroes.set_model(lsHeroes)
    
    if _heroPath.strip() != "" :
        populate_combobox(_heroPath, cbHeroes, lsHeroes)

    cellHero = gtk.CellRendererText()
    cbHeroes.pack_start(cellHero, True)
    cbHeroes.add_attribute(cellHero, 'text', 0)

    btHeroes.connect("clicked", choose_directory, cbHeroes, lsHeroes, lbHeroPath)
    hbHeroes.pack_start(cbHeroes, False, False, 0)
    
    window_box.pack_start(hbHeroes, False, False, 0)
    
    btGenerate = gtk.Button("Generate Thumb")
    
    btGenerate.connect("clicked", preview_gen, _image, lbReactionPath, cbReaction, textbuffer, lbHeroPath, cbHeroes)
    
    window_box.pack_start(btGenerate, False, False, 0)
    window.add(window_box)
    window.show_all()
    gtk.main()

def close_plugin_window(ret):
    gtk.main_quit()

register(
          "gen_thumb",
          "Generate Video Thumbnail",
          "Generate obnoxious thumbnail related to dota for internet videos",
          "Elisson Andrade",
          "MIT license",
          "2024",
          "Generate Thumbnail",
          "*",
          [
              (PF_IMAGE, "image", "Input image", None),
              (PF_DRAWABLE, "drawable", "Input drawable", None),
              (PF_DIRNAME, "reactionPath", "Reactions directory", ""),
              (PF_DIRNAME, "heroPath", "Heroes directory", ""),
              (PF_STRING, "thumbText", "Thumb Text", "")
          ],
          [],
          gen_thumb, menu="<Image>/Filters")
main()
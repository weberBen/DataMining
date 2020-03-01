#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

import environment as Env
import sys, os
import querySystem.matrixOp as query
import threading
import concurrent.futures
import logging
from tkinter import messagebox
from traceback import format_exc
import os

#%%
from PIL import Image, ImageTk
from itertools import count

class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


#%%
class SearchParms:
    def __init__(self, query, max_number, ceil):
        self.queryTxt = query
        self.MaxNumberResults = max_number
        self.CeilResults = ceil
#%%
def thread_initVar(self_class, end_function):
    error = False
    msg = None
    
    try :
        info = Env.Info()
        env_obj = Env.setupEnv([__file__, sys.argv[0], os.getcwd()], info)
        self_class._env_obj = env_obj
        self_class._database = env_obj.Database
        self_class._wordsBag = env_obj.WordsBag
        self_class._Freq = env_obj.Frequency
        
        request = query.Request(env_obj.Database, env_obj.WordsBag, env_obj.Frequency, env_obj.getMatrixFolder())
        request.load("matrix_all")
        self_class._request = request
        
    except Exception as e:
        error = True
        msg = e, format_exc()
    
    end_function(error=error, e=msg)

def thread_search(self_class, parms, update_function, end_function):
    error = False
    msg = None
    
    try :
        response = self_class._request.search(parms.queryTxt, parms.MaxNumberResults)
        update_function(response)
    except Exception as e:
        error = True
        msg = e, format_exc()
    
    end_function(error=error, e=msg)

    
class App:
    def __init__(self):
        self._isLoading = False
        self._results_query = {}
        self._root = tk.Tk()
        self._initGui()
        self._loadDisplay = ImageLabel(self._root)
        self._assetsDirectory = Env.getPath([__file__, sys.argv[0], os.getcwd()], Env._ASSETS_FOLDER_NAME)
        self._filenameLoadingGif = os.path.join(self._assetsDirectory, "loading.gif")
        
        self._env_obj = None
        self._database = None
        self._wordsBag = None
        self._Freq = None
        self._request = None
    
    def _intiVar(self):
        self._loading()
        thread = threading.Thread(target = thread_initVar, args = (self, self._stoploading))
        thread.start()

    def _loading(self):
        self._isLoading = True
        self._loadDisplay.grid(column=0, row=0, sticky = tk.E+tk.N+tk.W+tk.S)
        self._loadDisplay.load(self._filenameLoadingGif)
    
    def _stoploading(self, error=False, e=None):
        self._loadDisplay.grid_forget()
        self._loadDisplay.unload()
        self._isLoading = False
        
        if error:
            logging.error(e)
            messagebox.showerror("Error", str(e))
            self._root.destroy()
            return None
    
    def _validateEntryNumber(self, action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed is None or len(value_if_allowed)==0:
            return True
        
        if value_if_allowed:
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    
    
    def _initGui(self):
        self._root.geometry("950x700") 
        self._root.title("Télémagouilleur")
        self._root.grid_rowconfigure(1, weight=1)
        self._root.grid_columnconfigure(0, weight=1)
        
        self._vcmd = (self._root.register(self._validateEntryNumber),
                '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        
        self._search_group = tk.LabelFrame(self._root, text="SEARCH BOX")
        self._search_group.grid(column=0, row=0, pady=20, sticky = tk.N+tk.S+tk.W+tk.E)
        self._search_group.grid_rowconfigure(0, weight=1)
        self._search_group.grid_rowconfigure(1, weight=1)
        self._search_group.grid_rowconfigure(2, weight=1)
        self._search_group.grid_columnconfigure(0, weight=1)
        
        self._search_box = tk.Entry(self._search_group)
        self._search_box.grid(column=0, row=0, rowspan = 2, sticky = tk.W+tk.E+tk.N+tk.S)
        self._search_box.bind('<Return>', self._search)
        self._search_box.bind('<Control-a>', self._selctAll)
        
        
        wdgt = self._search_box
        column = wdgt.grid_info()['column']+wdgt.grid_info()['columnspan']
        row = wdgt.grid_info()['row']
        rowspan = wdgt.grid_info()['rowspan']
        columnspan = 2
        
        self._search_button = tk.Button(self._search_group, text="search", command=self._search)
        self._search_button.grid(column=column , row=row , rowspan=rowspan, columnspan = columnspan, sticky = tk.W+tk.E+tk.N+tk.S)
        
        
        wdgt = self._search_button
        column = wdgt.grid_info()['column']+wdgt.grid_info()['columnspan']
        row = wdgt.grid_info()['row']
        rowspan = 1
        columnspan = 2
        
        label = tk.Label(self._search_group, text="Results max number")
        label.grid(column=column , row=row , rowspan=rowspan, columnspan = columnspan)
        
        self._search_nb_results = tk.Entry(self._search_group, validate = 'key', validatecommand = self._vcmd)
        self._search_nb_results.grid(column=column , row=row+1 , rowspan=rowspan, columnspan = columnspan)
        self._search_nb_results.bind('<Control-a>', self._selctAll)
        
        column = column + self._search_nb_results.grid_info()['columnspan']
        label = tk.Label(self._search_group, text="ceil")
        label.grid(column=column , row=row , rowspan=rowspan, columnspan = columnspan)
        
        self._search_ceil_result = tk.Entry(self._search_group, validate = 'key', validatecommand = self._vcmd)
        self._search_ceil_result.grid(column=column , row=row+1, rowspan=rowspan, columnspan = columnspan)
        self._search_ceil_result.bind('<Control-a>', self._selctAll)
        #%%
        wdg = self._search_group
        row = wdg.grid_info()['row'] + wdg.grid_info()['rowspan']
        self._search_meta = tk.LabelFrame(self._root, text="SEARCH META")
        self._search_meta.grid(column=0, row=row, sticky = tk.W+tk.E+tk.N+tk.S)
        self._search_meta.grid_rowconfigure(0, weight=1)
        self._search_meta.grid_rowconfigure(1, weight=1)
        self._search_meta.grid_rowconfigure(2, weight=1)
        self._search_meta.grid_columnconfigure(0, weight=1)
        self._search_meta.grid_columnconfigure(1, weight=1)
        self._search_meta.grid_columnconfigure(2, weight=1)
        self._search_meta.grid_columnconfigure(3, weight=1)
        
        column = 0
        row = 0
        
        label = tk.Label(self._search_meta, text="Query")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        
        self._search_meta_query_txt = tk.Text(self._search_meta, height=5)
        self._search_meta_query_txt.grid(column=column+1, row=row, columnspan=2, rowspan=1, sticky= tk.W+tk.E)
        self._search_meta_query_txt.config(state='disabled')
        
        wdg = self._search_meta_query_txt
        column=wdg.grid_info()['column'] + wdg.grid_info()['columnspan']
        
        label = tk.Label(self._search_meta, text="Max number results")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        
        self._search_meta_max_results = tk.Label(self._search_meta, text="")
        self._search_meta_max_results.grid(column=column, row=row+1, sticky = tk.W+tk.E)
        
        wdg = self._search_meta_max_results
        column=wdg.grid_info()['column'] + wdg.grid_info()['columnspan']
        
        
        label = tk.Label(self._search_meta, text="ceil score results")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        
        self._search_meta_ceil_results = tk.Label(self._search_meta, text="")
        self._search_meta_ceil_results.grid(column=column, row=row+1, sticky = tk.W+tk.E)
        
        
        wdg = self._search_meta_query_txt
        column = 0
        row=wdg.grid_info()['row'] + wdg.grid_info()['rowspan']
        
        
        label = tk.Label(self._search_meta, text="Filtered query")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        
        self._search_meta_filtered_query_txt = tk.Text(self._search_meta, height=5)
        self._search_meta_filtered_query_txt.grid(column=column+1, row=row, columnspan=2, rowspan=1, sticky= tk.W+tk.E)
        self._search_meta_filtered_query_txt.config(state='disabled')
        
        
        wdg = self._search_meta_filtered_query_txt
        row=wdg.grid_info()['row'] + wdg.grid_info()['rowspan']
        
        label = tk.Label(self._search_meta, text="Actual results number")
        label.grid(column=0, row=row, sticky = tk.W+tk.E)
        
        self._search_meta_actual_results_number = tk.Label(self._search_meta, text="")
        self._search_meta_actual_results_number.grid(column=1, row=row, sticky = tk.W+tk.E)
        #%%
        wdg = self._search_meta
        row = wdg.grid_info()['row'] + wdg.grid_info()['rowspan']
        self._result_box = tk.LabelFrame(self._root, text="SEARCH RESULTS")
        self._result_box.grid(column=0, row=row, sticky = tk.W+tk.E+tk.N+tk.S)
        self._result_box.grid_rowconfigure(0, weight=1)
        self._result_box.grid_rowconfigure(1, weight=1)
        self._result_box.grid_columnconfigure(0, weight=1)
        self._result_box.grid_columnconfigure(1, weight=1)
        
        
        self._result_listbox = tk.Listbox(self._result_box)
        self._result_listbox.grid(column=0, row=1, sticky = tk.W+tk.E+tk.N+tk.S)
        self._result_listbox.bind('<Double-1>', self._dbclick)
        self._result_listbox.bind('<Return>', self._dbclick)
        
        
        
        self._movie_box = tk.LabelFrame(self._result_box, text="MOVIE INFO")
        self._movie_box.grid(column=1, row=1, padx=5, sticky = tk.W+tk.E+tk.N+tk.S)
        self._movie_box.grid_rowconfigure(0, weight=1)
        self._movie_box.grid_rowconfigure(1, weight=1)
        self._movie_box.grid_columnconfigure(0, weight=1)
        self._movie_box.grid_columnconfigure(1, weight=1)
        
        
        column = 0
        row = 0
        
        label = tk.Label(self._movie_box, text="Score")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        self._movie_score_label = tk.Label(self._movie_box)
        self._movie_score_label.grid(column=column+1, row=row)
        
        
        row+=1
        label = tk.Label(self._movie_box, text="BD id")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        self._movie_id_label = tk.Label(self._movie_box)
        self._movie_id_label.grid(column=column+1, row=row)
        
        label = tk.Label(self._movie_box, text="BD id")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        self._movie_id_label = tk.Label(self._movie_box)
        self._movie_id_label.grid(column=column+1, row=row)
        
        row+=1
        label = tk.Label(self._movie_box, text="Title")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        self._movie_title_label = tk.Label(self._movie_box)
        self._movie_title_label.grid(column=column+1, row=row)
        
        row+=1
        label = tk.Label(self._movie_box, text="Summary")
        label.grid(column=column, row=row, sticky = tk.W+tk.E)
        self._movie_summary = tk.Text(self._movie_box)
        self._movie_summary.grid(column=column+1, row=row, sticky = tk.W+tk.E+tk.N+tk.S)
        self._movie_summary.config(state='disabled')

    def _dbclick(self, event):
        item = self._result_listbox.get('active')  #get clicked item
        if item is not None and item!="":
            self._updateMovieSheet(self._results_query[item])
    
    def _updateMovieSheet(self, data):
        movie_id, score = data
        
        try :
            if int(self._movie_id_label["text"])==movie_id: #already displayed
                return None
        except ValueError:
            pass
        
        db = self._database.openNew()#thread safe
        
        movie = db.getMovie(movie_id)
        
        self._movie_score_label.config(text=str(score))
        self._movie_id_label.config(text=movie.id)
        self._movie_title_label.config(text=movie.title)
        self._updateText(self._movie_summary ,movie.summary)
        
    def _updateText(self, Text, txt):
        Text.config(state='normal')
        Text.delete('1.0', tk.END)
        Text.insert(1.0, txt)
        Text.config(state='disabled')


    #%% SEARCH BOX
    def _clearMovieDatasheet(self):
        self._movie_score_label.config(text="")
        self._movie_id_label.config(text="")
        self._movie_title_label.config(text="")
        self._updateText(self._movie_summary ,"")
    
    def _clearMetaSearch(self):
        self._updateText(self._search_meta_query_txt, "")
        self._updateText(self._search_meta_filtered_query_txt, "")
        self._search_meta_max_results.config(text="")
        self._search_meta_ceil_results.config(text="")
        self._search_meta_actual_results_number.config(text="0")
    
    def _clearResults(self, meta=False):
        self._result_listbox.delete(0, tk.END)
        self._results_query = {}
        self._clearMovieDatasheet()
        
        if meta:
            self._clearMetaSearch()
    
    def _getSearchParms(self):
        nbr = self._search_nb_results.get()
        ceil = self._search_ceil_result.get()
        query = self._search_box.get()
        
        try:
            nbr = int(nbr)
            if nbr==0:
                return None
            pass
        except ValueError:
            return None
            
        
        try:
            ceil = float(ceil)
            pass
        except ValueError:
            return None
        
        if query is None or len(query)==0:
            query = None
        
        return SearchParms(query, nbr, ceil)
    
    def _updateSearch(self, response):
        self._clearResults(meta=False)
        db = self._database.openNew()
        
        results = response.results
        self._search_meta_actual_results_number.config(text=str(len(results)))
        for res in results:
            movie_id, sco = res[0], res[1]
            
            movie = db.getMovie(movie_id)
            item = str(movie.title)+" (score="+str(sco)+")"
            self._results_query[item] = (movie.id, sco)
            self._result_listbox.insert('end', item)
        
        print("res=", str(response.filteredQuery))
        self._updateText(self._search_meta_filtered_query_txt, str(response.filteredQuery))
        self._result_listbox.focus()
    
    def _startSearch(self, parms):
        self._loading()
        thread = threading.Thread(target = thread_search, args = (self, parms, self._updateSearch, self._stoploading))
        thread.start()
    
    def _search(self, event=None):
        #result_label_search.itemconfigure(iptext, text=search_box.get())
        #result_label_search.create_text(100,10,fill="darkblue",font="Times 20 italic",text=search_box.get())
        if self._isLoading:
            return None
        
        parms = self._getSearchParms()
        if parms is None:
            logging.debug("Invalid parms given in GUI")
            messagebox.showerror("Error", "Invalid parms (number results and/or score ceil) given")
            return None
        
        if parms.queryTxt is None :
            self._clearResults(meta=True)
            return None
        
        search_txt = parms.queryTxt
        self._search_box.delete(0, 'end')
        self._updateText(self._search_meta_query_txt, search_txt)
        self._search_meta_max_results.config(text=self._search_nb_results.get())
        self._search_meta_ceil_results.config(text=self._search_ceil_result.get())
        
        self._startSearch(parms)
        
        
    def _selctAll(self, event):
        # select text
        self._root.after_idle(event.widget.icursor, 'end')
        self._root.after_idle(event.widget.select_range, 0, 'end')
        # move cursor to the end
    
    def run(self):
        self._intiVar()
        self._root.bind_all('<Escape>', lambda a : self._search_box.focus())
        self._search_box.focus()
        self._root.mainloop()

#%%

app = App()
app.run()
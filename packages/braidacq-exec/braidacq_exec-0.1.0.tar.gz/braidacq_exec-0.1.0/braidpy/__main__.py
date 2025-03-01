import argparse
import re
from time import time
from copy import copy

from braidpy.simu import simu
import pdb
import os
from tornado.ioloop import IOLoop
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
import cProfile
import pstats

# Définir le navigateur par défaut comme Chrome
os.environ["BOKEH_BROWSER"] = "chromium"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', default=1, type=int, help='Number of simulations')
    parser.add_argument('-s', default=None, type=str, help='String to identify')
    parser.add_argument('--stim_file', default=None, type=str, help='file containing all the stimuli to be read in one line separated by space. Incompatible with the graphic option')
    parser.add_argument('--unit', default=None, type=str, help='Reading unit')
    parser.add_argument('--att_phono_auto', action='store_true', default=None, help='Phonological attention position automatically calculated grom the grpahemic segmentation')
    parser.add_argument('--segment_reading', action='store_true', default=None, help='If True, creneau attention instead of gaussian')
    parser.add_argument('--new_phoneme', action='store_true', default=None, help='uses new phonemes to replace groups of 2 phonemes in one grapheme')
    parser.add_argument('-m', default=None, type=int, help='Max number of iterations')
    parser.add_argument('-l', default=None, type=str, help='language : en or fr')
    parser.add_argument('--lexicon', default=None, type=str, help='lexicon name')
    parser.add_argument('-f', default=None, type=str, help='fixed frequency of the stimulus')
    parser.add_argument('-t', default=None, type=str, help='Type of simulation')
    parser.add_argument('--fMin', default=None, type=float, help='min frequency to accept word in the lexicon')
    parser.add_argument('--maxItem', default=None, type=int, help='max word number in the lexicon')
    parser.add_argument('--maxItemLen', default=None, type=int, help='max word number per length in the lexicon')
    parser.add_argument('--fMinPhono', default=None, type=float, help='min frequency to accept word in the phonological lexicon')
    parser.add_argument('--fMinOrtho', default=None, type=float, help='min frequency to accept word in the orthographic lexicon')
    parser.add_argument('-v', default=None, type=str, help='Version of the lexical decision')
    parser.add_argument('-p', default=None, type=int, help='position of eye/attention')
    parser.add_argument('-g', action='store_true', help='graphic interface')
    parser.add_argument('--Qa', default=None, type=float, help='Value of Qa parameter')
    parser.add_argument('--sdA', default=None, type=float, help='Value of sdA parameter')
    parser.add_argument('--sdM', default=None, type=float, help='Value of sdM parameter')
    parser.add_argument('--p_sem', default=None, type=int, help='Value of p_sem parameter')
    parser.add_argument('--N_sem', default=None, type=int, help='Value of N_sem parameter')
    parser.add_argument('--thr_expo', default=None, type=float, help='exposition threshold during visual exploration')
    parser.add_argument('--stop', default=None, type=str, help='stop criterion for the simulation')
    parser.add_argument('--thr_fix', default=None, type=float, help='fixation threshold during visual exploration')
    parser.add_argument('--alpha', default=None, type=float, help='motor cost during visual exploration')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--TD', default=None, type=bool, help='orthographic top down retroaction')
    parser.add_argument('--TDPhono', default=None, type=bool, help='phonological top down retroaction')
    parser.add_argument('--phono', default=True, type=bool)
    parser.add_argument('--noContext', action='store_false', default=None, help='desactivation of context')
    parser.add_argument('--level', default=None, type=str, help='log level (info, debug)')
    parser.add_argument('--time', action='store_true', default=None, help='profiles time to execute')
    parser.add_argument('--fix_times', default=None, type=str, help='if simu_type=="change_pos", gives the times of fixations ex "0 300"')
    parser.add_argument('--fix_pos', default=None, type=str, help='if simu_type=="change_pos", gives the positions of fixations ex "0 2"')
    parser.add_argument('--remove_stim_ortho', action='store_true', default=None, help='remove the stimulus ortho from the lexicon')
    parser.add_argument('--remove_stim_phono', action='store_true', default=None, help='remove the stimulus phono from the lexicon')
    parser.add_argument('--remove_neighbors', action='store_true', default=None, help='remove the stim neighbors (ortho and phono) from the lexicon')
    parser.add_argument('--remove_lemma', action='store_true', default=None, help='remove the words that share lemma with the stim from the lexicon')
    parser.add_argument('--build_prototype', action='store_true', default=None, help='used if you want to build the prototype from the data file')
    parser.add_argument('--shift', action='store_true', default=None, help='comparison with left shift and right with length +1/-1')
    parser.add_argument('--explicit', action='store_true', default=None, help='explicit learning : choose to create/update at the right time, with right word updated')
    parser.add_argument('--semi-explicit', action='store_true', default=None, help='explicit learning : choose to create/update at the right time, with most probable word updated')
    parser.add_argument('--mixture_knowledge', action='store_true', help='uses a mixture of ortho representations : expert, child and unknown')
    parser.add_argument('--n_choose_word', default=None, type=int, help='Number of nearest words chosen')

    args = parser.parse_args()
    if "stim_file" in args and args.stim_file is not None:
        with open(args.stim_file, 'r') as file:
            content = file.read()
        words_list = content.split()

    def get_param(dico, liste):
        return dict(**{value: getattr(args, key) for key, value in dico.items() if getattr(args, key) is not None},
                    **{value: getattr(args, value) for value in liste if getattr(args, value) is not None})
    simu_param = get_param({'m': 'max_iter', 't': 'simu_type', 'stop': 'stop_criterion_type', 'unit': 'reading_unit'},
                           ['level', 'build_prototype', 'thr_expo', 'segment_reading'])
    simu_args = get_param({}, ['thr_fix', 'alpha', 'n_choose_word'])
    if simu_args is not None:
        simu_param['simu_args'] = simu_args
    model_param = get_param({'lexicon': 'lexicon_name', 'v': 'version', 'l': 'langue', },
                            ['shift', 'new_phoneme'])  # ,'force_app','force_update','force_word'])
    ortho_param = get_param({'s': 'stim', 'Qa': 'Q', 'sdA': 'sd', 'TD': 'top_down', 'remove_stim_ortho': 'remove_stim', 'explicit': 'force_word', 'fMinOrtho': 'fMin'},
                            ['sdM', 'fMinOrtho', 'remove_lemma', 'remove_neighbors'])
    phono_param = get_param({'TDPhono': 'top_down', 'remove_stim_phono': 'remove_stim', 'phono': 'enabled', 'fMinPhono': 'fMin'},
                            ['fMinPhono', 'remove_lemma', 'remove_neighbors', 'att_phono_auto'])
    semantic_param = get_param({'noContext': 'context_sem'}, ['p_sem', 'N_sem'])
    if simu_param['simu_type'] == "change_pos":
        simu_args['times'] = [int(i) for i in args.fix_times.split()]
        simu_args['pos'] = [int(i) for i in args.fix_pos.split()]
    if args.p is not None:
        simu_param['pos_init'] = args.p

    # lenMin and lenMax set according to the length of the stimulus to optimize memory
    # ortho_param['lenMin']=len(ortho_param['stim'])-1
    # ortho_param['lenMax']=len(ortho_param['stim'])+1
    # phono_param['lenMin']=len(ortho_param['stim'])-1
    # phono_param['lenMax']=len(ortho_param['stim'])+1
    sim = simu(model_param, ortho_param, phono_param, semantic_param, **simu_param)
    if sim.simu_type == "change_pos":
        sim.fix = {"t": simu_args['times'], "pos": simu_args['pos']}
    if args.f is not None:
        sim.model.change_freq(args.f, sim.stim)
    if args.g:
        def modify_doc(doc):
            GUI = gui(sim)
            for att in dir(doc):
                try:
                    setattr(doc, att, getattr(GUI.curdoc, att))
                except:
                    pass

        # avoid unnecessary storage in almost all conditions besodes GUI
        sim.store_dist['ortho'] = ['percept', 'word']
        sim.store_dist['phono'] = ['percept', 'word']
        sim.run_simu_general()
        # Créez une instance de l'application Bokeh en utilisant la fonction de rappel
        io_loop = IOLoop.current()
        # Créez une instance du serveur Bokeh avec l'application Bokeh
        server = Server(applications={'/': Application(FunctionHandler(modify_doc))}, io_loop=io_loop, port=5001)
        server.start()
        server.show('/')
        io_loop.start()
        io_loop.stop()
    else:
        if args.time:
            pr = cProfile.Profile()
            pr.enable()
            cProfile.runctx("for i in range(args.n): print('n=',i); sim.run_simu_general()", {'sim': sim, 'args': args}, {}, 'tmp.txt')
            print(pstats.Stats('tmp.txt').strip_dirs().sort_stats('time').print_stats(50))
        else:
            if args.stim_file:
                copy_model = copy.deepcopy(sim.model)
                for i in words_list:
                    sim.model = copy.deepcopy(copy_model)
                    sim.model.stim = i
                    sim.run_simu_general()
            else:
                for i in range(args.n):
                    print('n=', i)
                    if args.explicit or args.semi_explicit:
                        if i == 0:
                            sim.model.ortho.force_app = True
                        else:
                            sim.model.ortho.force_app = False
                            sim.model.ortho.force_update = True
                    sim.run_simu_general()
    if args.debug:
        pdb.set_trace()


def hook():
    import tkinter as tk
    from tkinter import font
    from tkinter import ttk

    def pron_to_ipa(string):
        string = string.replace('#', '').replace('~', '')
        # ipa = pd.read_csv(os.path.join(_ROOT, "resources/chardicts/xsampa_fr.csv"), encoding="utf-8")[['char', 'ipa']]
        # ipa['ipa'] = ipa['ipa'].astype(str)
        # return "".join([str(ipa[ipa.char == i].ipa.values[0]) for i in string])
        return string

    def run(result_label,stim_entry):
        def simu_calculation():
            try:
                sim = simu(model_param, ortho_param, phono_param, semantic_param, **simu_param)
                sim.run_simu_general()
                phi = ("Correct" if sim.model.phono.percept.evaluate_decision(dist_name="percept") else "incorrect") + f" pronunciation: " + pron_to_ipa(sim.one_res('phi'))
                wphi = ("Correct" if sim.model.phono.word.evaluate_decision() else "incorrect") + f" word identification: {pron_to_ipa(sim.one_res('wphi'))}"
                time = f"Duration: {sim.t_tot} iterations\n"
                ortho_trace = "Orthographic representation " + ("created" if sim.model.ortho.word.PM else "updated")
                phono_trace = "Phonological representation " + ("created" if sim.model.phono.word.PM else "updated")
                context_list = sim.model.semantic.context_sem_words
                context_words = "Context words: " + ("None" if not entry_context.get() else '\n \t' + "\n \t".join(" ".join(context_list[i:i + 5]) for i in range(0, len(context_list), 5)))
                result_label.config(text=phi + "\n" + wphi + "\n" + time + "\n" + ortho_trace + "\n" + phono_trace + "\n" + context_words)
            except :
                # Si une erreur quelconque se produit, afficher "Error" dans l'interface
                result_label.config(text="Error: Check terminal for details")
                # Afficher l'erreur détaillée dans le terminal
                import traceback
                traceback.print_exc()
        simu_param, model_param, ortho_param, phono_param, semantic_param, _ = {}, {}, {}, {}, {}, {}
        new_stim=''.join(re.findall(r'[a-zA-Zàáâãäåæçèéêëìíîïðñòóôõöøùúûüÿ]', str(entry_stim.get()))).lower()[:12]
        ortho_param['stim'] = new_stim
        stim_entry.delete(0, tk.END)
        stim_entry.insert(0, new_stim)
        label_stim.config(text=new_stim)
        model_param['langue'] = str({"French": "fr", "German": "ge", "English": "en"}[entry_langue.get()])
        phono_param['remove_stim'] = entry_remove_stim_phono.get()
        ortho_param['remove_stim'] = entry_remove_stim_ortho.get()
        semantic_param['context_sem'] = entry_context.get()
        result_label.config(text="Running ...")
        root.after(100, simu_calculation)

    def rb_binary(title, left, right):
        frame = tk.Frame(root, bd=1, relief="raised")
        frame.pack(expand=True)
        label_remove_stim = tk.Label(frame, text=title)
        label_remove_stim.pack(expand=True)
        entry_remove_stim = tk.BooleanVar()
        r1 = tk.Radiobutton(frame, text=left, value=True, variable=entry_remove_stim)
        r2 = tk.Radiobutton(frame, text=right, value=False, variable=entry_remove_stim)
        r1.pack(side="left")
        r2.pack(side="right")
        return entry_remove_stim

    def resize_widgets(parent):
        new_font = font.Font(family='Arial', size=18)
        for widget in parent.winfo_children():
            try:
                if isinstance(widget, tk.Frame):
                    resize_widgets(widget)
                widget.config(font=new_font)  # Appliquer la nouvelle police
            except tk.TclError:
                pass  # Certains widgets peuvent ne pas supporter la police

    root = tk.Tk()
    root.geometry('500x700')
    _ = root.title("Reading with the BRAID-Acq model")

    frame_stim = tk.Frame(root, bd=1, relief="raised")
    frame_stim.pack(expand=True)
    label_stim = tk.Label(frame_stim, text="Stimulus:")
    label_stim.pack(expand=True)
    entry_stim = tk.Entry(frame_stim)
    entry_stim.pack(expand=True)

    entry_remove_stim_phono = rb_binary("Phonologically", "novel", "known")
    entry_remove_stim_ortho = rb_binary("Orthographically", "novel", "known")
    entry_context = rb_binary("Context", "present", "absent")

    frame_lang = tk.Frame(root, bd=1, relief="raised")
    frame_lang.pack(expand=True)
    labelChoix = tk.Label(frame_lang, text="Language")
    labelChoix.pack(expand=True)
    listeLang = ["French", "English"]#, "German"]
    entry_langue = ttk.Combobox(frame_lang, values=listeLang, state="readonly")
    entry_langue.current(0)
    entry_langue.pack(expand=True)

    result_label = tk.Label(root, text=" ", justify="left")
    calc_button = tk.Button(root, text="Run", command=lambda: run(result_label,entry_stim))
    calc_button.pack(expand=True)
    result_label.pack(expand=True)

    resize_widgets(root)

    root.mainloop()

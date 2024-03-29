# this app allows filtering epoched data.
# it loads the epoched data, applies a bandpass filter to it using the parameters specified in the config.json file
# it then saves the filtered data and plots the filter response
# it also saves a report of the filtered data

import os
import mne
import json
import helper
import matplotlib.pyplot as plt
from mne.viz import plot_filter, plot_ideal_filter
import re

#workaround for -- _tkinter.TclError: invalid command name ".!canvas"
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load brainlife config.json
with open('config.json','r') as config_f:
    config = helper.convert_parameters_to_None(json.load(config_f))

# == LOAD DATA ==
fname = config['epo']
epo = mne.read_epochs(fname, preload=True)
epo_orig = epo.copy()
sfreq = epo.info['sfreq']
f = mne.filter.create_filter(epo_orig.get_data(),
                             sfreq,
                             l_freq=config['l_freq'],
                             h_freq=config['h_freq'],
                             filter_length=config['filter_length'], 
                             l_trans_bandwidth=config['l_trans_bandwidth'],
                             h_trans_bandwidth=config['h_trans_bandwidth'],
                             method=config['method'],
                             iir_params=config['iir_params'], 
                             phase=config['phase'],
                             fir_window=config['fir_window'],
                             fir_design=config['fir_design'])

plt.figure()
fig=plot_filter(f,sfreq)
plt.savefig(os.path.join('out_dir_figs','filter_response.png'))

if config['notch']:
    config['notch'] = [int(x) for x in re.split("\\W+",config['notch'])]
    raw.notch_filter(freqs=config['notch'], picks=config['picks'])

epo.filter(picks=config['picks'], 
           l_freq=config['l_freq'],
           h_freq=config['h_freq'],
           filter_length=config['filter_length'],
           l_trans_bandwidth=config['l_trans_bandwidth'],
           h_trans_bandwidth=config['h_trans_bandwidth'],
           method=config['method'],
           iir_params=config['iir_params'],
           phase=config['phase'],
           fir_window=config['fir_window'],
           fir_design=config['fir_design'],
           skip_by_annotation=config['skip_by_annotation'],
           pad=config['pad'])
        

report = mne.Report(title='Filtering report')

report.add_figure(fig, title='Filter')

report.add_epochs(epo_orig, 'Original unfiltered data', psd=True)

report.add_epochs(epo, 'Filtered data', psd=True)

report.save('out_dir_report/report_filter.html', overwrite=True)


epo.save('out_dir/meg-epo.fif',overwrite=True)

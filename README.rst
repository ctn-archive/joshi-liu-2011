Spatiotemporal processing and coincidence detection
===================================================

The aim of this project was to connect the retina and the cochlea to
Nengo and create a co-incidence detector. We get information from jAER
using UDP packets, and we can feed this into the coincidence detector
we've created in Nengo. The detector will light up if orientations
from the retina and 48 channels of the cochlea are all active. Results
A coincidence detector was created the layout of this is shown below,
as can be seen it's a tree like structure where a thresholding unit is
created and then cascaded with multiplier units. Code to help
interface the retina to other networks, with a small spatiotemporal
filtering example is here. This is used by the sparse coding model in
this archive.

This archive contains the following python scripts and some matlab data files.

1) auditory_in.py
2) just_UDP.py
3) matlab_io.py

The just_UDP.py file was the file I'd written for Sam that would get
inputs from JAER, most of it is just Sam's code, the UDP part is mine,
I think Tobi's got a copy of the code somewhere. The auditory_in.py
file was an attempt at multimodal sensory fusion. The idea behind it
is as follows. The third one is the temporal gabor, I never did get
around to finishing it, but it does seem to work, I need to put this
together to be more than a 1-D spatial gabor first.

The input layer consist of twelve input populations that get inputs
from the cochlea, these are simple populations, with weighted
connections to threshold units, the aim of these threshold units is to
fire only if all inputs are active (the weights of these units are one
set of parameters that need tweaking a larger population size could
probably result in much better noise resilience as well) The output of
these are then fed into a multiplier tree, consisting of cascaded two
input multipliers (performing an and). The output should spike only if
the input spikes, due to some reason the spikes end up attenuating as
they traverse the populations and sometimes input spikes are
missed. This is an error I've still not managed to rectify. For the
third file, I still need to think about how exactly I want to create
an MxN spatial Gabor, but once that's implemented this code does the
temporal Gabor using the feedback idea we'd spoken about.

Contact info
------------

Siddharth Joshi
sijoshi at ucsd

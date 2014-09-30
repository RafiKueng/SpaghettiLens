#Install Glass on OpenSUSE

##0. Prereq.

###Get the basics you should have anyways:
(ipython is not needed, but can be handy later on)

    sudo zypper install git python ipython

###Get some developper stuff:
(this should also install `blas-devel gcc48-fortran gcc-fortran lapack-devel`)

    sudo zypper install --type pattern devel_basis
    sudo zypper install swig python-devel python-numpy-devel

###Get the science stuff

    sudo zypper install numpy

The scipy in repro has a bug (import error _fblas), we use pip to compile the latest:

    sudo zypper install python-pip
    sudo pip install scipy

(takes a few minutes. If you already have scipy use `sudo pip install scipy --upgrade`)

... and the plotting.. There is still a missing backend used by default.
    sudo zypper install python-matplotlib
    sudo zypper install python-matplotlib-tk


(Note to devs maybe thats actually a bug? fix it with:

    import matplotlib
    matplotlib.use("Agg")

and / or use `echo 'backend : Agg' > matplotlibrc` in root (where `run_glass` is)


For the rendering of the plot labels, you'll need latex. There are two options:


* install everything huge and easy:
this will give you the full package including docs, but uses up 1GB of diskspace..

    sudo zypper install texlive-latex

* small and handpicked:
This gives you a smaller package (150mb; you can further squeeze it if you like..):

    sudo zypper install --no-recommends texlive-latex texlive-type1cm texlive-psnfss texlive-dvips



##1. Get glass

    cd ~/src
    git clone git@github.com:RafiKueng/glass.git
    cd glass
    make
    make
    

##2. test glass with the example

    cd Example
    ../run_glass B1115.gls

this should return in a *.state file

    ../run_glass ../Tools/viewstate.py B1115.state
    
this should show fancy plots

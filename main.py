from typing import Any
from matplotlib import pyplot as plt
import matplotlib.colors as mlc
from scipy.stats import qmc
from dataclasses import dataclass
import numpy as np
import copy

@dataclass
class shape:
  l: float = 1.
  cx: float = 0.0
  cy: float = 0.0
  nx: int = 100
  ny: int = 100
  ax: Any = None
  ps: np.ndarray = None 
  ns: int = 10
  al: float = -50.
  au: float=50.
  state: np.ndarray = None
  newState: np.ndarray = None
  X: np.ndarray = None
  Y: np.ndarray = None
  
  def prepare_figure(self):
    fig = plt.gcf()
    self.ax = fig.add_subplot(1, 1, 1)
    self.ax.set_xlim(0, self.nx, 1.)
    self.ax.set_ylim(0, self.ny, 1.)
    # And a corresponding grid
    self.ax.grid(which='both')
    # Or if you want different settings for the grids:
    self.ax.axes.xaxis.set_ticklabels([])
    self.ax.axes.yaxis.set_ticklabels([])
    self.ax.grid(which='minor', alpha=0.2)
    self.ax.grid(which='major', alpha=0.5)
    plt.ion()
    
  def draw_set(self):
    
    rectangle = plt.Rectangle((self.cx,self.cy), self.l, self.l, fc='black',ec="black")
    self.ax.add_patch(rectangle)
  
  def generate_samples(self):
    l_bounds = [0]*self.nx
    u_bounds = [1]*self.nx

    sampler = qmc.LatinHypercube(self.nx)
    sample = sampler.random(n=self.ny)
    self.state = copy.deepcopy(qmc.scale(sample, l_bounds, u_bounds)) 
    self.state = copy.deepcopy(np.round(self.state))

  def fill_space(self):
    x = np.linspace(self.al+self.l/2., self.au-self.l/2., self.nx)
    y = x = np.linspace(self.al+self.l/2., self.au-self.l/2., self.ny)
    self.X, self.Y = np.meshgrid(x, y)
    # self.generate_samples()
    self.state = np.random.choice([0,1], size=(self.nx, self.ny), p=[.5, 0.5])
    self.newState = copy.deepcopy(self.state)
  
  def update_figure(self):
    img = np.zeros((self.nx, self.ny), dtype=float)
    color_map = mlc.LinearSegmentedColormap.from_list('ColorMap', [(1.000, 1.000, 1.000), (0.0, 0.0, 0.0)])
    self.ax.imshow(self.state, cmap=color_map, interpolation='none')
    plt.pause(0.001)
    for i in range(self.nx):
      for j in range(self.ny):
        try:
          a = self.state[i-1, j]
        except:
          a = 0
        try:
          b = self.state[i+1, j]
        except:
          b = 0
        try:
          c = self.state[i, j-1]
        except:
          c = 0
        try:
          d = self.state[i, j+1]
        except:
          d = 0
        try:
          e = self.state[i-1, j-1]
        except:
          e = 0
        try:
          f = self.state[i+1, j-1]
        except:
          f = 0
        try:
          g = self.state[i-1, j+1]
        except:
          g = 0
        try:
          h = self.state[i+1, j+1]
        except:
          h = 0
        n_live: int = a + b + c + d + e + f + g + h
        if self.state[i, j] == 1:
          if n_live <= 1 or n_live >= 4:
            self.newState[i, j] = 0
        else:
          if n_live == 3:
            self.newState[i, j] = 1
    self.state = copy.deepcopy(self.newState)
    self.ax.cla()
    self.ax.imshow(self.newState, cmap=color_map, interpolation='none')
    self.ax.draw
    plt.pause(0.001)

  def run_GOL(self):
    try:
      while True:
        self.update_figure()
    except KeyboardInterrupt:
      pass

def main():
  s = shape()
  s.ns = 8
  s.fill_space()
  s.prepare_figure()
  s.run_GOL()

main()


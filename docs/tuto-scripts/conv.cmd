for %%f in (run_aa_*.png) do (
  composite -gravity center overlay.png %%f tmp.png
  convert tmp.png -crop 1280x720+0+280 n_%%f
  
)
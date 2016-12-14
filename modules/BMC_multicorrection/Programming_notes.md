# Programming notes of BMC_multicorrection
##  1. Functions in BMC_multicorrection_design.ui
**apply2mirror**: apply the pattern onto mirror   
**acquireImage**: acquire a single snapshot or a stack with the camera    
**calc_image_metric**: calculate the existing image's metric    
**syncRawZern**: update self.raw_MOD by synchronizing all the zernike modes in the list.    
**toDMSegs**: pass self.raw_MOD to self.control and convert to segments.    
**setZern_ampli**: set zernike amplitudes   
**setZern_step**: set zernike stepsize    
**updateZern**: update zernike coefficients and syncRawZern   
**single_Evaluate**: evaluate sharpness of the figure without changing any parameters     
**step_Hessian**: Create a Hessian matrix. First row: the derivative. second-to-last row: the Hessian.    

## 2. Error logs    
1- connection error of the piezo stage (does not appear anymore)    
2- MultiDM doesnot allow a direct reset of the mirror.  Must add the function into the module DM_core.    
3- Replace the measurement of stacks with the measurement of snapshots. 

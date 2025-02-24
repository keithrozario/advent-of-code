The original solution I had tried to iterate through all possible 4 change iterations. Each number could change a maximum of -9 to 9, and had 18 possible values. Hence the total combiations was 18^4.

This was large and I tried to whittle it down, by only iterating through 'possible' iterations (i.e. iterations where the sum of all changes was between -9 and 9). This didn't help much, there were still many possible iterations.

Instead, I reversed the problem. I stored every change value into a dict and did a lookup. Everytime I encountered a 4-series change for a monkey, I updated that value in a dict. 

At the end all I had to do was find the max value in the dict (since we already summed it for all monkeys). This made the program run much much faster.
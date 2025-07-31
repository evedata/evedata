# Why make this?

After years of building EVE tools and watching countless projects die from data complexity or developer burnout, I realized we need more resilient infrastructure. Our ecosystem already has incredible data sources - Adam4EVE's market data, EVERef's comprehensive item database, Fuzzwork's industry calculations and data exports. These pillars have served the community for years, and EVEData isn't trying to replace them.

Instead, I'm building EVEData to be another strong node in this network - helping distribute the load, providing redundancy, and maybe exploring some new approaches to data access. The more of us maintaining quality data sources, the more resilient our ecosystem becomes. Plus, I want to experiment with some ideas around unified APIs, real-time streams, and making complex data correlations simpler.

Think of it this way: if you want to build a tool that analyzes market trends across regions, you currently need to set up ESI polling, handle error limits, store historical data, load a Fuzzwork SDE conversion or parse it yourself for type information, and probably grab kill data to understand demand. That's weeks of work before you even start on your actual idea. With EVEData, that should be a single API call.

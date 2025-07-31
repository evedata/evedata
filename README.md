# EVEData Platform 🚧

**Status: Under active construction**

Hey there! You've found the EVEData platform repository. This is where I'm building the data infrastructure that I wish existed when I started developing tools for EVE Online.

## What is EVEData?

EVEData is my attempt to solve a problem that's frustrated me for years: accessing EVE's data shouldn't be this hard. Every developer building tools for EVE ends up solving the same problems over and over again. We all write our own SDE parsers, build our own caching and error limiting-aware clients for ESI, create our own historical data stores, and wrestle with combining multiple data sources just to answer simple questions.

I'm building EVEData to be a unified data platform that handles all of this complexity once, so developers can focus on building amazing tools instead of fighting with data pipelines.

## Why am I building this?

After years of building EVE tools and watching countless projects die from data complexity or developer burnout, I realized we need more resilient infrastructure. Our ecosystem already has incredible data sources - Adam4EVE's market data, EVERef's comprehensive item database, Fuzzwork's industry calculations and data exports. These pillars have served the community for years, and EVEData isn't trying to replace them.

Instead, I'm building EVEData to be another strong node in this network - helping distribute the load, providing redundancy, and maybe exploring some new approaches to data access. The more of us maintaining quality data sources, the more resilient our ecosystem becomes. Plus, I want to experiment with some ideas around unified APIs, real-time streams, and making complex data correlations simpler.

Think of it this way: if you want to build a tool that analyzes market trends across regions, you currently need to set up ESI polling, handle error limits, store historical data, load a Fuzzwork SDE conversion or parse it yourself for type information, and probably grab kill data to understand demand. That's weeks of work before you even start on your actual idea. With EVEData, that should be a single API call.

## How does it work?

This monorepo contains the beating heart of EVEData: the ESI scrapers, SDE loaders, data pipelines, ETL processes, and infrastructure that keep everything running. Here's what's happening behind the scenes:

I'm leveraging (and honing) the experience I have from my day job building distributed systems and data products at scale to build a robust data architecture that continuously syncs with EVE's data sources (ESI, SDE, and more), cleans and transforms that raw data and creates useful aggregates, and then makes it available through modern APIs. Everything is designed to be cost-efficient, maintainable by myself as its sole developer, and reliable enough for production use.

The architecture leverages a combination of cloud providers and bare metal for performance and cost-effectiveness to handle EVE's data volumes, and implements careful reliability mechanisms to be a responsible ESI citizen.

## Current focus

Right now, I'm deep in the foundational work: building robust ESI synchronization, creating an efficient data model, setting up the infrastructure for analytical and operational data storage, and designing the initial APIs. It's not glamorous, but getting these fundamentals right is important for everything that comes next.

## Want to follow along?

EVEData is being built in the open. You can watch the progress, see the struggles, and eventually contribute to making EVE's data more accessible for everyone. Check out the [Vision document](VISION.md) to understand where this is all heading.

Fair warning: things are messy right now. I'm prioritizing getting core functionality working over perfect code. Once the foundation is solid, I'll circle back to clean things up and make it easier for others to contribute.

## Questions?

Feel free to open a [discussion topic](https://github.com/evedata/evedata/discussions) if you're curious about something specific. I'm building this for the community, so community input is always welcome. Just remember that this is a solo project built in my spare time, so progress comes in bursts between real life responsibilities.

## License

Except as otherwise noted, the code in this repository is licensed under the [MIT License](https://opensource.org/licenses/MIT) (see [LICENSE-CODE](https://github.com/evedata/evedata/blob/main/LICENSE)) and the documentation content (`docs/content`) in this repository is licensed under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/legalcode) (see [LICENSE-DOCS](https://github.com/evedata/evedata/blob/main/LICENSE)).

"EVE", "EVE Online", "CCP", and all related logos and images are trademarks or registered trademarks of CCP hf.

# EVEData Project Vision

## Vision

**"A New Eden where every developer can build game-changing tools and every player can access the data they need to excel."**

## Mission

To provide the fastest, most reliable, and developer-friendly data platform for EVE Online, offering access to real-time and historical game data with unique analytics and insights through modern data products that eliminate infrastructure complexity and enable rapid tool development.

## Reality check

EVEData is a solo passion project built in my free time with a strict infrastructure budget that allows me to bootstrap it for the foreseeable future out of my own pocket. Outside of its goal to contribute to the EVE ecosystem, it's also my vehicle for continuously improving my skills and staying current with the technologies I use day to day. I'm committed to progress on EVEData that will be steady but measured, and I'll be transparent about what's possible within these boundaries.

## What EVEData is (and isn't)

EVEData will begin its life as an API-first platform focused on solving for foundational data access and integration problems that third-party developers and players have. It's initial focus will be on creating a reliable data lakehouse with unified access to market data, kill data, industrial data, and historical information through modern, performant APIs and community access to both raw and curated datasets.

As the platform matures and proves sustainable, EVEData will thoughtfully expand into user-facing tools where it can add unique value. This could eventually include a new killboard with novel analytics, market tools with unique insights, or multi-character industrial planning tools with rich connections to live data. I'll build these expansions only when EVEData can offer something meaningfully different while maintaining its core infrastructure excellence.

EVEData won't become an alliance or corporation management platform like [Alliance Auth][alliance-auth] or [SeAT][seat]. It won't have tools for managing members, SRP, or fleet operations. While it may eventually offer premium capabilities that cost ISK for things like multi-character industry and asset management and corporation/alliance analytics, these will focus on intelligence and insights, not operational management. EVEData is about understanding and analyzing what happens in New Eden, not administering organizations within it.

## Core values

### 1. Developer experience first

I'm building EVEData because I've felt the frustration of wrestling with the SDE and ESI and juggling multiple data sources when building EVE tools. Every project decision starts with making life easier for developers and players who want access to EVE's data. This means performant, intuitive APIs that work on the first try without complicated OAuth flows, documentation that helps understand the data, and examples that solve real problems.

### 2. Trust through transparency

As a new project in an ecosystem sustained by community pillars like [Adam4EVE][adam4eve], [EVERef][everef], [Fuzzwork][fuzzwork], and [zKillboard][zkillboard] but also littered with abandoned projects. I know trust in a new community service needs to be earned, and I'm committed to open source and transparency from day one, with regular development updates (even when progress is slow), and honest communication about any challenges. When I make mistakes, I'll own them publicly.

### 3. Performance within constraints

While operating on a shoestring budget, I'm committed to delivering the best performance possible within those constraints. This means sustainable, boring technology choices, efficient data engineering, and pragmatic optimization choices. I'll benchmark everything and share metrics openly.

### 4. Sustainable by design

Too many EVE tools die from developer burnout or unsustainable economics. EVEData is designed to run indefinitely with my own income, with infrastructure costs eventually offset by an ad- and/or donation-based monetization strategy. Code will be well-tested, written for maintainability, and all systems will be documented for future contributors (or in the worst case future stewards). All of EVEData's repositories and project documentation will be open source and permissively licensed and, once the project matures past its initial release, a community contribution model will be established.

### 5. Community driven and thoughtfully executed

The best features will come from community pain points, but will still be balanced with technical feasibility and project scope. I'll actively engage with developers and players, celebrate tools built on the platform, and contribute back to the ecosystem whenever possible. However, focus is essential for a solo project and not every request will make it to the roadmap.

### 6. Progressive complexity

EVE's first-party data ecosystem is inherently complex, but accessing it doesn't have to be. EVEData will offer simple endpoints for common needs while exposing powerful capabilities for advanced users. A new developer should be able to get market data in minutes, while an alliance tool developer can access complex historical analytics.

### 7. Pragmatic innovation

Innovation for EVEData means solving real problems better, not chasing technology trends. I'll choose boring, proven technologies that will still work in five years. Success is measured by delighting EVEData's users, not creating architectural novelty. If EVEData can reduce the time to build a new market analysis tool from weeks to hours, the platform has succeeded.

### 8. Data integrity above convenience

The data provided by EVE's first-party sources like ESI and the SDE is inherently messy. EVEData commits to transparently giving users the information they need to account for data quality issues at every layer. Quality metadata will be provided for all datasets that includes indicators like confidence scores for derived values, freshness indicators, and completeness metrics for aggregated statistics. All of EVEData's transformations, aggregations, and calculations will be thoroughly documented. Logs and metrics from EVEData's ingestion and data processing pipelines will also be available to view at any time on publicly-available dashboards.

### 9. Privacy is non-negotiable

While EVEData will require authentication for resource management and abuse prevention, it will never collect more than the minimum data it needs to operate. Client information like the account and IP address that made a request will always be anonymized. Usage data that could indirectly give the ability to identify a user will be further [k-anonymized][k-anonymity] to prevent re-identification. If ads are implemented, only privacy-respecting providers that don't require user tracking will be considered, and if you choose to use an ad blocker, EVEData won't ever guilt you about it or degrade functionality. If you delete your account, all of your data will go with it immediately with no soft deletes. If EVEData ever introduces services that require ingestion of private data, end-to-end encryption measures will be designed so that your data can only ever be accessed by you, even if the platform ever suffers a security breach.

### 10. Responsible partnership

EVEData will always strive to be an exemplary partner in the EVE community, with or without official EVE Online Partner status. This especially means being a responsible API consumer that respects ESI limits and never architects to circumvent them. Being a good partner also means acknowledging and respecting other services in the ecosystem, even if they're competitors. EVEData will always seek to enhance the community by providing data products and services that help make everyone's tools better. Any future monetization strategy to help sustain the project will never violate the EVE Developer License Agreement, and any ad- or donation-based monetization will always be to grow and sustain the project, never for personal profit.

## Success metrics

### Year one goals

- 100+ daily active users using the platform
- 99.5% platform uptime
- Sub-100ms cached API response times
- Monthly infrastructure costs under ~$300 (offset by ad revenue and donations)
- 5+ community tools built on EVEData
- Included in [EVE's Community Showcase][eve-community]

### Long-term vision

- Become one of the de facto data sources for new EVE tools alongside other community pillars
- Active contributor community maintaining specialized data products built on the platform
- [EVE Online Partner][eve-partner] status

## Technical approach

EVEData will evolve iteratively with major capability milestones to keep it focused. As a solo project built with care rather than speed, development will progress organically and continuously incorporate community needs and technical learnings along the way. I won't impose artificial deadlines that compromise quality or personal sustainability.

Rather than promise dates, I'll provide full transparency about EVEData's current focus and progress. This will include a public changelog, roadmap, and status page, regular development logs, and places for community feedback like GitHub discussions and Discord.

### Authentication

Unlike most similar services in the ecosystem, EVEData's APIs and services will be available only to authenticated clients. This will allow for better cost control, performance management, and security from the platform's inception and remove the complexity of developing a system with partially-anonymous access. [Bearer tokens][token-authentication] will be used to authenticate all requests.

A user will log in through [EVE SSO][eve-sso] in order to verify their identity and establish an account. On initial release, EVEData's web UI will provide a developer console where a user can manage their [personal access tokens][pat] that can be used to access EVEData's resources, as well as associate additional characters with their account. Additional authorization flows may be developed in the future.

### Market data product

EVEData's first release will be its data product for live and historical order book data and statistics in all regions, trade hubs, and popular public structures. While the current ecosystem is crowded in this domain, working backwards from this milestone will result in a focused technical roadmap for bootstrapping EVEData's infrastructure and essential platform components like ESI ingestion, the data lakehouse architecture, the developer REST API and console, and developer access to raw and curated datasets as flat-files.

### Generative AI integration

EVEData arrives in the new age of generative AI and will embrace it where it can provide value to the community. Using the EVEData REST API as its backend, a Model Context Protocol (MCP) server will be released that will allow compatible Large Language Model (LLM) clients like Claude Desktop to use EVEData. This will allow users to make natural language queries to the platform like "What are the potential arbitrage opportunities between Jita and Amarr?" Queries to the MCP server will follow the same commitment to privacy described in the values above, and usage logs will always be fully anonymized.

### Market UI

After the initial REST API proves stable and useful, the web UI will be further developed from its initial token management experience to include market data reporting and visualization that prioritizes accessibility and mobile experience. The web UI itself will be a reference implementation for consuming EVEData's API and will evolve with the project as more capabilities are added.

### Real-time capabilities

With the market data product and UI complete, real-time capabilities will be added progressively for market data. These capabilities will include a unified websocket endpoint for real-time feeds and event subscriptions for webhooks, including an API and web UI portal to manage subscriptions. As with the initial release of the web UI, real-time capabilities will initially focus on market data.

### Additional core data products

Development of additional data products based on other raw ESI sources will begin once the platform foundation built for the market data product is stable. Work on only the raw ingestion pipelines for these data products may happen in parallel while building the initial market data product in order to have historical data when full development begins.

- **Markets**: Enhancements to initial market data product to include regional market history.
- **Contracts**: Public contracts with state and bid history with aggregated statistics.
- **Killmails**: Detailed statistics and analytics on killmails, using zKillboard's [RedisQ endpoint][zkillboard-redisq] for discovery.
- **Mapping**: Live and historical sovereignty, system jumps, system kills (enriched with killmail data).
- **Logistics**: live and historical route optimization and safety data.
- **Manufacturing**: Live and historical data on industry facilities, solar system cost indices, adjusted prices, raw bills of materials
- **Meta**: Live and historical ESI uptime and player count.

### Derived products

Once the core data products are in place, development will be possible of derived services that leverage co-location with the platform's data products to provide analytics and intelligence that would still be complex or expensive for users to do themselves. Potential services include arbitrage opportunity analysis, multi-character manufacturing plan optimization, contract and killmail doctrine matching, and trade route profitability analytics.

### Premium tiers and services

All of the data products and services that EVEData provides will always be available to every user, with clearly published rate limits to ensure fair use and platform stability. Once usage patterns at initially-set rate limits have been established, premium tiers for increased usage of services with high compute requirements and increased quotas on webhooks will also be made available.

Any premium tier introduced will use an ISK-based pricing model with automatic payment tracking and invoicing. EVE's Developer License Agreement prohibits real-world monetization and premium services will not be tied to EVEData's Patreon in any way. ISK revenue from EVEData's premium services will simply be income for my own characters and corporation in-game.

While EVEData's core purpose is to serve the community at large, once the project has matured there could be an opportunity to provide secure, private lakehouses and analytics for alliance and corporation-owned data like markets, contracts, and killmails as an ISK-paid service. Right now though, I'm focused on building EVEData as a way to democratize EVE's data for everyone.

## Getting involved

If you're as excited about this vision for a new EVE data platform as I am and want to watch the project as it progresses, you can keep an eye on any of these places:

- [@evedata.io](https://bsky.app/profile/evedata.io) on Bluesky
- [Discussions](https://github.com/evedata/discussions) on GitHub
- [Project tracking](https://github.com/orgs/evedata/projects/1) on GitHub
- [EVEData](https://discord.gg/G2Sks9H8) on Discord

o7

---

_These values and boundaries guide EVEData from day one. As a solo developer with limited resources, I'm choosing focus over features, sustainability over scale, and community trust over rapid growth._

[adam4eve]: https://www.adam4eve.eu/
[alliance-auth]: https://allianceauth.readthedocs.io/
[eve-community]: https://developers.eveonline.com/docs/community/
[eve-partner]: https://www.eveonline.com/partners
[eve-sso]: https://developers.eveonline.com/docs/services/sso/
[everef]: https://everef.net/
[fuzzwork]: https://www.fuzzwork.co.uk/
[k-anonymity]: https://en.wikipedia.org/wiki/K-anonymity
[pat]: https://en.wikipedia.org/wiki/Personal_access_token
[seat]: https://eveseat.github.io/docs/
[token-authentication]: https://datatracker.ietf.org/doc/html/rfc6750
[zkillboard]: https://zkillboard.com/
[zkillboard-redisq]: https://github.com/zKillboard/RedisQ

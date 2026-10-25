# Architecture decision records: extra sources

Fetched 2026-10-25 with curl and read as page text. Paraphrase only. Each row gives the URL, the org, and the clause of `code-adr` it backs.

1. https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html. AWS. Each ADR describes the decision, its context, and its consequences, and the collection forms a decision log. Backs the Rule.
2. https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record. Microsoft. An ADR records how and why the system took its shape, including alternatives ruled out. Include a problem statement with context, the options considered, the decision outcome, and the tradeoffs. Only include choices that affect structure or key quality attributes. Backs the Rule and the options clause in Why.
3. https://cloud.google.com/architecture/architecture-decision-records. Google. ADRs capture why decisions were made and which alternatives were decided against; the format includes context, key options, and the reasons for the accepted choice. Backs the Rule and the options clause in Why.
4. https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework. UK government (GOV.UK). Each ADR carries title, date, status, context, decision, consequences, stakeholders consulted, and links; review and update it when context or consequences change. Backs the Rule.
5. https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record. Spotify. A significant decision that affects how engineers write software gets an ADR, which captures the decision, the context, and the consequences. Backs the Rule.
6. https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions. Cognitect (Michael Nygard). Without the rationale and consequences, a later reader can only accept or reverse a decision blindly. Backs the Rule and the Why.

Count: AWS, Microsoft, Google, GOV.UK, Spotify, and Cognitect = 6 orgs behind the Rule. The options-ruled-out clause has Microsoft and Google, plus Hickey's talk and Orosz's post (individuals), so it sits in Why.

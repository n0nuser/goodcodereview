# How large firms and cloud providers audit an app, service or platform

Quotes were read on the live pages (fetch tool, 2026-10-31) unless marked UNREAD. Sections 1-4 of each framework are sourced facts. The final synthesis is inference.
Gaps are listed in "Sourcing gaps" at the end. Where a fetch tool summarised a page, only text it returned inside quotation marks is quoted here.

## 1. AWS Well-Architected Framework Review (WAFR), Lens, Tool, HRI/MRI

**Covers.** Six pillars; the framework "helps you understand the pros and cons of decisions you make while building systems on AWS" so you can design "secure, reliable, efficient, cost-effective, and sustainable workloads". Source: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html. A workload can also carry extra lenses: "Each lens has its own set of questions, best practices, notes, and improvement plan." Lenses are either "Lens Catalog" (AWS-maintained) or "Custom lenses" with "your own pillars, questions, best practices, and improvement plans"; "Five lenses can be added at a time to a workload, with a maximum of 20". Source: https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses.html

**How run.**
- "It should be a lightweight process (hours not days) that is a conversation and not an audit." "blame-free approach that encourages diving deep." Source: https://docs.aws.amazon.com/wellarchitected/latest/framework/the-review-process.html
- Cadence: "Reviews should be applied at key milestones in the product lifecycle, early on in the design phase ... and then before the go-live date." Teams are also advised to review "nearly continuous[ly]".
- Reviewing another team's workload: "a series of informal conversations about their architecture ... You can then follow up with one or two meetings". Logistics: whiteboards, diagram printouts, and an "Action list of questions that require out-of-band research to answer (for example, 'did we activate encryption or not?')".
- Tool: the AWS Well-Architected Tool "provides a consistent process for you to review and measure your architecture". AWS partners run reviews too (welcome page above).
- Basis: questions "verify that people don't neglect areas that often featured in Root Cause Analysis (RCA)".

**Evaluated.**
- "High risk issues (HRIs) ... are architectural and operational choices that AWS has found might result in significant negative impact to a business." "Medium risk issues (MRIs) also might negatively impact business, but to a lesser extent." Source: https://docs.aws.amazon.com/wellarchitected/latest/userguide/workloads.html
- Risks derive from your answers; the page calls them guidelines: "If there are specific technical or business reasons that prevent applying a best practice ... the risk might be lower than indicated." Customers should "document the applicable business level approval and reasons for not implementing it".
- Improvement status values: None, Not Started, In Progress, Complete, Risk Acknowledged.
- No sampling; the unit is the whole workload, answered by the team.

**Output.** Per-workload list of HRIs/MRIs and an improvement plan. "A milestone records the state of a workload at a particular point in time" and "A best practice is to save a milestone every time you make improvements" (https://docs.aws.amazon.com/wellarchitected/latest/userguide/milestones.html). The review yields "a list of issues that you can prioritize based on your business context". Re-test = update answers, save a new milestone. Cross-team: "identify any mechanisms, training, or principal engineering talks" for thematic issues.

## 2. Azure Well-Architected Review

**Covers.** Five pillars: "Reliability, Security, Cost Optimization, Operational Excellence, and Performance Efficiency". Each pillar has "recommended practices, risk considerations, and tradeoffs". Source: https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework

**How run.** "Microsoft Azure Well-Architected Review is offered at no charge. It's a collection of questionnaires tied to the pillar checklists to evaluate your design choices." (same page). The assessment landing page says: "Format: Multiple choice and multiple response questions." Source: https://learn.microsoft.com/en-us/assessments/azure-architecture-review/. Self-service, team-run. Workload guidance adds "an assessment that helps you evaluate your readiness in production".

**Evaluated.**
- Score: "Track your score through iterative runs to identify possible areas for enhancement." Azure's own guide (https://learn.microsoft.com/en-us/azure/well-architected/design-guides/implementing-recommendations) calls it "a self-assessment that helps a workload team examine a workload" with "approximately 60 questions", says "Set a cadence, for example every four months, and use milestones to track how the workload design can continue to improve", and "Use the milestone feature of the assessment to track this change over time, using the prior milestone as a baseline." Recommendations can be "postponed or dismissed". The scoring formula is not documented on any page read; the assessment landing page says only "Over time, you can improve your score by following these personalized recommendations." The Microsoft Assessments FAQ (https://learn.microsoft.com/en-us/assessments/support/) says the results page "will provide you with an overall score helping you benchmark where you are on your journey" plus "tailored recommendations per category". Results can be exported: "Assessment results can be exported to a CSV file". A separate "Go-Live | Well-Architected Review" assessment "helps you holistically evaluate an Azure workload in a go-forward motion across the five tenets" (30-60 minutes; https://learn.microsoft.com/en-us/assessments/azure-architecture-review/).
- Maturity model: "divided into five levels" per pillar. Level 1 "Establish a solid foundation on Azure", Level 2 "Build workload assets", Level 3 "Be production-ready", Level 4 "Learn from production", Level 5 "Future-proof with agility". "These boundaries are suggested guidelines and don't need to be taken as strict rules."
- "Treat that evaluation as a moving score that evolves with your workload."
- Prioritisation instead of blanket compliance: "Defer checklist items that are less relevant to your workload's success."

**Output.** "After completion of assessment, you will receive pragmatic recommendations based on your specific needs." (assessment page). Re-test is re-running the questionnaire and comparing scores.

## 3. Google Cloud Architecture Framework (Well-Architected Framework)

**Covers.** Six pillars: operational excellence, security/privacy/compliance, reliability, cost optimization, performance optimization, sustainability. A pillar "provides principles and recommendations for a specific non-functional focus area." Source: https://docs.cloud.google.com/architecture/framework

**How run.** The page offers no human review cadence. It ships material "To enable AI agents to evaluate your cloud workloads against the principles and recommendations in each pillar": "Assessment questions that agents can ask to understand the requirements of a workload" and "A validation checklist that agents can use to evaluate an architecture's alignment".

**Evaluated.** No rating scale or scoring. The page read in full (re-fetched 2026-10-31, "Last reviewed 2026-10-13 UTC") has no review cadence, maturity model or scoring method; the only assessment material is for agents, listed above.

**Output.** Not defined on the page read (guidance, assessment questions, validation checklist).

## 4. Microsoft SDL

**Covers.** Ten practices (https://www.microsoft.com/en-us/securityengineering/sdl/practices): "Establish security standards, metrics, and governance"; "Require use of proven security features, languages, and frameworks"; "Perform security design review and threat modeling"; "Define and use cryptography standards"; "Secure the software supply chain"; "Secure the engineering environment"; "Perform security testing"; "Ensure operational platform security"; "Implement security monitoring and response"; "Provide security training".

**How run.** Practices are embedded across the lifecycle by the engineering team (the page does not specify a separate auditor or cadence). Design stage: "ensure that the design doesn't naturally allow attackers to easily gain unauthorized access."

**Evaluated.** No ratings or levels on this page. The first practice names "metrics". The page does not mention a final security review.

**Output.** Not defined here (the page lists practices, not artifacts).

## 5. OWASP ASVS (levels 1-3)

**Covers.** Verification requirements grouped by chapter (v5.0: encoding, validation and business logic, web frontend, API, file handling, authentication, session, authorization, tokens, OAuth/OIDC, cryptography, communication, configuration, data protection, secure coding and architecture, logging and errors, WebRTC). Count: "The ASVS is made up of a total of around 350 requirements which are divided into 17 chapters" (https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x03-What-is-the-ASVS.md); the chapter names listed come from the file listing at https://github.com/OWASP/ASVS/tree/master/5.0/en, not a page quote.

**How run.** Verifier picks a level and scope. Techniques "may require access to documentation, source code, configuration, and the people" involved, beyond penetration testing with valid credentials. "Certifying organizations can choose their testing methods but should disclose them in the report and this should ideally be repeatable." OWASP "does not certify any vendors, verifiers, or software." Source: https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x04-Assessment_and_Certification.md

**Evaluated.** Levels (https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x03-What-is-the-ASVS.md):
- L1: "minimum requirements ... This level contains around 20% of the ASVS requirements."
- L2: "Most applications should be striving to achieve this level" ... "an application needs to implement around 70% of the requirements in the ASVS (all of the L1 and L2 requirements)".
- L3: "should be the goal for applications looking to demonstrate the highest levels of security and provides the final ~30% of requirements".
- Level choice by risk: "an early-stage startup ... may decide to focus on Level 1 ... but a bank may have difficulty justifying anything less than Level 3".

**Output.** "an ASVS certification report should include scope, a summary of all requirements checked, the requirements where exceptions were noted, and guidance on resolving issues." This contrasts with pen-test reports that list failures "by exception". The verifier "should make the scope of the verification clear including which Level the organization is attempting to" reach.

## 6. OWASP SAMM (maturity)

**Covers.** "OWASP SAMM defines five business functions and fifteen security practices": Governance (Strategy & Metrics, Policy & Compliance, Education & Guidance); Design (Threat Assessment, Security Requirements, Secure Architecture); Implementation (Secure Build, Secure Deployment, Defect Management); Verification (Architecture Assessment, Requirements-driven Testing, Security Testing); Operations (Incident Management, Environment Management, Operational Management). Source: https://owaspsamm.org/model/

**How run.** "Start with a self-assessment to get an overview of the status of software security activities in your organization." It can be run "together with other people involved in your software development process"; the Toolbox has an "Interview" tab with questions per activity; "Evaluate whether these criteria are met. If they are not completely fulfilled, answer 'No'." Source: https://owaspsamm.org/assessment/. Tooling: spreadsheet Toolbox, SAMMwise, SAMMY.

**Evaluated.** Maturity levels 1-3 per practice, e.g. Strategy and Metrics: "Identify objectives and means of measuring effectiveness of the security program." (1), "Establish a unified strategic roadmap for software security within the organization." (2), "Align security efforts with the relevant organizational indicators and asset values." (3). Source: https://owaspsamm.org/model/governance/strategy-and-metrics/. "the Scorecard tab updates automatically with your current maturity score."

**Output.** Scorecard plus a roadmap: "use the Toolbox to create and track your own SAMM roadmap." Re-test is a repeat assessment against the roadmap.

## 7. NIST SSDF (SP 800-218 v1.1)

**Covers.** "The practices are organized into four groups": Prepare the Organization (PO), Protect the Software (PS), Produce Well-Secured Software (PW), Respond to Vulnerabilities (RV). PO: "ensure that their people, processes, and technology are prepared to perform secure software development". PS: "protect all components of their software from tampering and unauthorized access". RV: "identify residual vulnerabilities in their software releases and respond appropriately". Source (PDF, text extracted locally): https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf

**How run.** Not an audit. It is a vocabulary: "software purchasers and consumers can also use it to foster communications with suppliers in acquisition processes" (abstract, https://csrc.nist.gov/pubs/sp/800/218/final). Each practice has tasks plus "Notional Implementation Examples" and references; the document says the examples are "a starting point". Conformance is attested by the supplier (the document refers to how "each provider will attest to their conformance with the agreement").

**Evaluated.** No ratings or levels in the publication. Goal stated: "reduce the number of vulnerabilities in released software, mitigate the potential impact of the exploitation of undetected or unaddressed vulnerabilities, and address the root causes".

**Output.** Supplier attestation or an acquisition-process evidence package; no report shape defined by SP 800-218 itself.

## 8. SOC 2 (AICPA Trust Services Criteria)

**Covers.** Five categories: "controls over security, availability, processing integrity, confidentiality, and privacy" (https://www.aicpa-cima.com/resources/download/get-description-criteria-for-your-organizations-soc-2-r-report). An exam covers "the description of the service organization's system in accordance with the description criteria" and "the suitability of design and operating effectiveness of controls based on the applicable trust services criteria" (https://www.aicpa-cima.com/resources/article/addressing-additional-subject-matter-and-criteria-in-soc-2-r-engagement). The AICPA guide references the "2017 trust services criteria" and "2018 description criteria" (https://www.aicpa-cima.com/cpe-learning/publication/soc-2-reporting-on-an-examination-of-controls-at-a-service-organization-relevant-to-security-availability-processing-integrity-confidentiality-or-privacy).

**How run.** A licensed CPA firm (service auditor) examines; management supplies a system description and assertion. The illustrative Type 2 report "meets the reporting requirements of SSAE-21" (https://www.aicpa-cima.com/resources/download/illustrative-service-auditors-soc-2-r-type-2-report); its contents (assertion, description, auditor's report, tests of controls and results) are not readable without login; see gaps.

**Evaluated.** Type 1 vs Type 2: "For a type 1, the service auditor is evaluating controls as of a specific date." (AICPA quoting a practitioner, https://www.aicpa-cima.com/professional-insights/video/maintaining-high-standards-for-soc-engagements). Type 2 adds operating effectiveness over a period; the page read only says "in type 2 report, the operating effectiveness" and the period length (commonly 6-12 months) came from third-party snippets and is UNSOURCED here. AICPA's guide page (read in Chrome, https://www.aicpa-cima.com/cpe-learning/publication/soc-2-reporting-on-an-examination-of-controls-at-a-service-organization-relevant-to-security-availability-processing-integrity-confidentiality-or-privacy) describes "Assertion-based examination of a service organization's description of its system and its controls" but gives no period wording. Opinion is an auditor judgement, not a numeric score.

**Output.** Auditor's report containing the description, management assertion and, for Type 2, tests of controls and results. Exceptions appear in the results; re-test = next period report.

## 9. ISO/IEC 27001 certification audit

**Covers.** An information security management system (ISMS). ISO's own pages (read in Chrome, 2026-10-31): "ISO/IEC 27001 is the world's best-known standard for information security management systems (ISMS). It defines requirements an ISMS must meet." Source: https://www.iso.org/standard/27001. ISO/IEC 27006-1:2024 "specifies the additional requirements for bodies that audit and certify information security management systems (ISMS) in accordance with ISO/IEC 27001. It complements ISO/IEC 17021-1" (https://www.iso.org/standard/82908.html). ISO/IEC 17021-1 (https://www.iso.org/standard/61651.html): "Certification of management systems is a third-party conformity assessment activity". Those ISO pages do not describe Stage 1/Stage 2 or finding grades; the standard text is paid and the ISO Online Browsing Platform preview needs acceptance of Terms of Use, which was not done. A certification body's own guidebook (BSI, a major certification body, not a standard body) is used for process. 

**How run.** Source: BSI management systems guidebook, https://www.bsigroup.com/siteassets/pdf/en/insights-and-media/insights/brochures/aunz-as-scert-govn-built-qua-mpd-mp-pp168managementsystemsguidebook-0626.pdf (PDF text extracted locally).
- "The purpose of the Stage 1 audit is to assess your organisation's readiness for certification." BSI reviews management system documentation; "Any areas of concern identified during the Stage 1 audit must be" resolved before Stage 2.
- "The purpose of the Stage 2 (Certification) Audit is to determine whether your organisation's management system has been effectively implemented and complies with the requirements of the relevant standard ... by reviewing actual practices, documentation, and records".
- "Certification is maintained through an ongoing audit cycle, typically spanning three (3) years. This cycle consists of two surveillance audits, conducted annually, followed by a recertification audit."

**Evaluated.** Findings "are categorised as Major, Minor, or Opportunities for" improvement.
- Major: "indicate a breakdown in the effectiveness or integrity of the management system ... needs to be closed or downgraded to a minor non-conformance before certification can be granted."
- Minor: "isolated instances of non-compliance that do not compromise the overall integrity of the management system".
- Both need a corrective action plan "including correction, root cause analysis, and proposed long-term actions ... within two (2) weeks".
- Major/minor grading: the ISO pages only say 27006-1 complements ISO/IEC 17021-1; the grading rule itself is read only in BSI's guidebook (certification-body practice, not ISO text).

**Output.** Audit report with graded findings, CAPs, a certification decision, a certificate valid three years. Major closeout "verified onsite or remotely".

## 10. ISACA COBIT and ITGC audits (Big4)

**Covers.** COBIT is "the premier framework for the governance and management of enterprise IT" with "40 governance/management objectives" (https://www.isaca.org/resources/cobit). ITGC areas as sold by EY: "Access Management – user account administration, authentication, access recertification, and privileged accounts", "Change Management – documentation, approval, testing, and deployment of system changes", and "data backup and recovery, scheduled tasks, monitoring, patch management, and vulnerability management" (https://www.ey.com/en_cz/services/technology-risk/it-audit-readiness-and-implementation-assessment-of-it-controls).

**How run.** COBIT 2019 capability assessment has four steps: "Introduce COBIT 2019 to Stakeholders and Establish Assessment Awareness", "Tailor the Enterprise Program and Process", "Rate Process Activities", "Obtain Assessment Results". Ratings "are rated subjectively, based on interviews with stakeholders, reviews of executed procedure documents, oversight programs and execution of an enterprise's goals and objectives." Source: https://www.isaca.org/resources/news-and-trends/industry-news/2020/effective-capability-and-maturity-assessment-using-cobit-2019. EY offers ITGC work "as part of external financial statement audits and as internal audit engagements", including "gap analysis against ISA and SOX standards" (EY page).

**Evaluated.** "the capability and maturity levels are measured between 0 and 5" and "Performance management in COBIT 2019 is based on the CMMI Performance Management Scheme" (https://www.isaca.org/resources/news-and-trends/industry-news/2020/cobit-2019-and-cobit-5-comparison). Levels 1-5: Initial, Managed, Defined, Quantitively Managed, Optimizing. Per-activity ratings use "fully, largely, partially, or not". Cut-offs, from ISACA (https://www.isaca.org/resources/news-and-trends/industry-news/2019/defining-target-capability-levels-in-cobit-2019-a-proposal-for-refinement): "Fully (F)—The capability level is achieved for more than 85 percent."; "Largely (L)—The capability level is achieved between 50 percent and 85 percent."; "Partially (P)—The capability level is achieved between 15 percent and 50 percent."; "Not (N)—The capability level is achieved less than 15 percent." The 2020 ISACA article says only that the descriptors "have varying percentages assigned to each one".

**Output.** Capability/maturity profile per objective; for audit use, ITGC deficiency conclusions feeding the financial-statement auditor. Big4 pages read in Chrome: PwC offers "IT General Control (ITGC) Monitoring and Testing" covering "access to programs and data, program change, and computer operations controls", with testing outputs generated "on a periodic (e.g., quarterly) basis" (https://www.pwc.com/us/en/services/managed-services/cyber-risk-regulatory/application-security-and-controls.html). KPMG names "Weak access controls over system administration", "Inadequate change management" and "Inadequate IT governance and oversight" as themes behind adverse ICFR assessments (https://kpmg.com/us/en/articles/2024/it-controls-and-icfr.html). Deloitte describes "gaining assurance on controls pertaining to internal, regulatory and extended enterprise requirements" (https://www.deloitte.com/global/en/services/consulting-risk/services/it-and-specialised-assurance-services.html); that page has no ITGC method. The UK variant (https://www.deloitte.com/uk/en/services/risk-advisory/services/it-and-specialised-assurance-services.html) offers "design and operating effectiveness reviews for IT General Controls". Deloitte US (https://www.deloitte.com/us/en/services/audit-assurance/blogs/accounting-finance/internal-controls-material-weakness-prevention.html): "Material weaknesses related to GITC failures have increased significantly every year since 2021."; it describes no ITGC test method. Deloitte Malta (https://www.deloitte.com/mt/en/services/audit-assurance/perspectives/mt-it-controls-for-smes.html) names domains: "logical access controls to prevent or detect unauthorised use of and changes to, data, systems, or programs", "changes to the network, application systems and database management systems are implemented in a controlled manner", and for SaaS providers "assurance is typically obtained through service organisation control (SOC) reports". ISACA glossary (https://www.isaca.org/resources/glossary) has no "IT general controls" entry; it defines "General computer control" as "A control, other than an application control, that relates to the environment in which computer-based application systems are developed, maintained and operated and is therefore applicable to all applications."

## 11. CIS Benchmarks and CIS Controls (IG1-3)

**Covers.** Benchmarks are "prescriptive configuration recommendations for more than 25+ vendor product families" and a "consensus-based effort of cybersecurity experts globally" (https://www.cisecurity.org/cis-benchmarks). Controls v8/v8.1 have "a total of 153 Safeguards" (https://www.cisecurity.org/controls/implementation-groups).

**How run.** Tooling: "CIS-CAT Pro Assessor" to "Assess system conformance to CIS Benchmarks" (benchmarks page). Automated configuration scan against a published baseline; no interview step on the page.

**Evaluated.** Implementation Groups (IG page): IG1 is "essential cyber hygiene", "the foundational set of cyber defense Safeguards that every enterprise should apply"; IG2 "builds upon IG1"; IG3 "is comprised of all the Controls and Safeguards." Benchmark profiles (CIS Benchmarks FAQ, read in Chrome, https://www.cisecurity.org/cis-benchmarks/cis-benchmarks-faq): "The Level 1 profile is considered a base recommendation that can be implemented fairly promptly and is designed to not have an extensive performance impact." "The Level 2 profile is considered to be "defense in depth" and is intended for environments where security is paramount." The FAQ also names a STIG profile.

**Output.** CIS-CAT Pro HTML report (https://ciscat-assessor.docs.cisecurity.org/en/latest/ReportHTML/): "For a recommendation to reach an overall Pass result, *all* checks/tests must result in a Pass." Result types Pass, Fail, Error, Unknown, Manual ("This recommendation cannot be fully automated and requires manual evaluation."); Percent is "Percent of recommendations passed in a given section ((Score/Max)*100)", and "All scored recommendations currently have a weight of 1." IG assessments give safeguards implemented per group (not quoted).

## 12. DORA metrics (State of DevOps)

**Covers.** Delivery performance, not an audit checklist. Five metrics (https://dora.dev/guides/dora-metrics/). Throughput: "Change lead time" ("the amount of time it takes for a change to go from committed to version control to deployed in production"), "Deployment frequency", "Failed deployment recovery time". Instability: "Change fail rate" ("The ratio of deployments that require immediate intervention following a deployment"), "Deployment rework rate".

**How run.** Computed from the delivery pipeline and incident data per application/service, by the team or a platform group. The page read does not set a cadence or who runs it.

**Evaluated.** The metrics guide (https://dora.dev/guides/dora-metrics/) sets no thresholds: "Top performers do well across all five metrics, and low performers do poorly." The DORA FAQ (https://dora.dev/faq/) says "before 2018, we consistently found three clusters (Low, Medium, High)", "we found only three" in 2022, and that the reports "found four clusters" in 2023 and 2024. Clusters are not fixed bands: "We have never dictated the number of clusters; they are emergent from the patterns in the data." Numeric thresholds are per-year: the 2022 report PDF (https://dora.dev/research/2022/dora-report/2022-dora-accelerate-state-of-devops-report.pdf, text extracted locally) gives Low/Medium/High as deployment frequency "Between once per month and once every 6 months" / "Between once per week and once per month" / "On-demand (multiple deploys per day)", and change failure rate "46%-60%" / "16%-30%" / "0%-15%". It dropped the elite cluster: "This year's high cluster is a blend of last year's high and elite clusters." The 2023 report landing page frames them as a starting point: "Using metrics to understand strengths and weaknesses is a starting point." The 2023 and 2024 report PDFs were too large or unreadable (see gaps).

**Output.** Trend per metric, used for comparison over time, not a findings report.

## 13. Google SRE Production Readiness Review (PRR)

**Covers.** Source: https://sre.google/sre-book/evolving-sre-engagement-model/. Reviewers assess maturity across "architecture and interservice dependencies, monitoring, emergency response, capacity planning, change management, and performance" (re-fetched: the page introduces the list with "SRE is concerned with several aspects of a service, which are collectively referred to as production."; the items quoted under How run are the page's own text, but the page does not say PRR reviewers assess exactly these).

**How run.** Source (read in Chrome): https://sre.google/sre-book/evolving-sre-engagement-model/ . "SRE initiates a Production Readiness Review with the development team." Phases, verbatim headings: Engagement, Analysis, Improvements and Refactoring, Training, Onboarding, Continuous Improvement. Engagement: "Usually one to three SREs are selected or self-nominated to conduct the PRR process." Analysis: "Usually, the SRE team establishes and maintains a PRR checklist explicitly for the Analysis phase." and "SREs also look at recent incidents and postmortems for the service, as well as follow-up tasks for the incidents." Improvements: "The priorities are discussed and negotiated with the development team, and a plan of execution is agreed upon." Axes reviewed: "System architecture and interservice dependencies", "Instrumentation, metrics, and monitoring", "Emergency response", "Capacity planning", "Change management", "Performance: availability, latency, and efficiency". Example checklist item: "Are all user-visible request failures well instrumented and monitored, with suitable alerting configured?" Three models: Simple PRR (post-launch), Early Engagement (design onward), Frameworks and SRE Platform ("Onboarding each service required two or three SREs and typically lasted two or three quarters" before frameworks). No rating scale: the outcome is an SRE team accepting the pager or not.

**Evaluated.** Checklist against production best practices plus incident history. No numeric rating on the page.

**Output.** Prioritised, jointly negotiated fix list; the gate is operational handover: once improvements are sufficient, "an SRE team assumes its production responsibilities." Launch checklist (read in Chrome): https://sre.google/sre-book/launch-checklist/ is Appendix E, "Google's original Launch Coordination Checklist, circa 2005, slightly abridged for brevity". Its top-level headings are "Architecture", "Machines and datacenters", "Volume estimates, capacity, and performance", "System reliability and failover", "Monitoring and server management", "Security", "Automation and manual tasks", "Growth issues", "External dependencies" and "Schedule and rollout planning". In https://sre.google/sre-book/reliable-product-launches/ a dedicated team does the review: "Members of the LCE team audit services at various times during the service lifecycle." and acts as "gatekeepers and signing off on launches determined to be "safe""; the checklist "helps an LCE assess the launch and provides the launching team with action items". The workbook chapter (https://sre.google/workbook/engagement-model/) says "Proposed changes from ARR and PRR must be prioritized jointly by the developers and the SREs." It is a one-off pre-launch list, not a rated review.

## 14. Accessibility data point: W3C WCAG-EM

Source: https://www.w3.org/TR/WCAG-EM/. Covers a website against WCAG 2.2. Five steps: "Define the evaluation scope", "Explore the target product", "Select a representative sample set", "Evaluate the selected sample set", "Report the findings". Sampling: structured sample of "common views, essential functionality" plus a random sample; "The number of samples to randomly select is 10% of the structured sample set". Report: "Include at least the following" sections "About the evaluation," "Evaluation scope," "Digital product exploration," "Representative sample set," "Sample set evaluated". Caveat: "using this methodology alone does not result in being able to make WCAG 2 conformance claims."

## 15. Privacy data points: GDPR Art. 35 DPIA and NIST Privacy Framework

GDPR Art. 35 (https://gdpr-info.eu/art-35-gdpr/): trigger is processing "likely to result in a high risk to the rights and freedoms of natural persons"; the controller must assess "prior to the processing". Mandatory cases include "a systematic and extensive evaluation of personal aspects ... based on automated processing, including profiling", "processing on a large scale of special categories of data", and "a systematic monitoring of a publicly accessible area on a large scale". Minimum content: a systematic description of the processing and purposes; "an assessment of the necessity and proportionality"; "an assessment of the risks to the rights and freedoms of data subjects"; and "the measures envisaged to address the risks". No rating scale in the Article. It is run by the controller, per processing operation, before launch.

NIST Privacy Framework (https://www.nist.gov/privacy-framework/getting-started-0, read in Chrome): "a voluntary tool intended to help organizations identify and manage privacy risk". Three parts: "Core, Profiles, and Implementation Tiers". Five Functions: "Identify-P, Govern-P, Control-P, Communicate-P, and Protect-P". Tiers "reflect a progression from informal, reactive responses to approaches that are agile and risk informed" ; the tier names come from the framework PDF (https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.01162020.pdf, text extracted locally): "There are four distinct Tiers, Partial (Tier 1), Risk Informed (Tier 2), Repeatable (Tier 3), and Adaptive (Tier 4)". "The Tiers represent a progression, albeit not a compulsory one.". Profiles are not ratings: "The Core is not a checklist of actions to perform".

---

# Cross-cutting synthesis (INFERENCE, not sourced facts)

## Common anatomy

scope -> criteria -> evidence -> test -> rate -> report -> remediate -> retest

| Step | Examples in the sources above |
|---|---|
| Scope | WCAG-EM "Define the evaluation scope"; ASVS verifier states level and scope; SOC 2 system description; WAFR workload |
| Criteria | Pillar questions (AWS/Azure), ASVS requirements, Trust Services Criteria, ISO standard, SRE PRR checklist |
| Evidence | Interviews (SAMM, COBIT, WAFR), documents and records (ISO Stage 2, ASVS), tool scans (CIS-CAT), incident history (PRR) |
| Test | Design vs operating effectiveness (SOC 2 Type 1 vs 2), sample sets (WCAG-EM), technical verification (ASVS) |
| Rate | See table below |
| Report | ASVS scope plus checked list plus exceptions; WCAG-EM report sections; SOC 2 auditor's report; ISO report with graded findings |
| Remediate | AWS improvement plan; ISO CAP within two weeks; PRR negotiated fixes; SAMM roadmap |
| Retest | AWS milestones; Azure score reruns; ISO surveillance and recertification; SOC 2 next period |

Two stances exist. Self-service and "conversation, not an audit" (AWS, Azure, SAMM, PRR) versus independent third-party attestation (SOC 2, ISO, ASVS verification, Big4 ITGC). The second stance adds a formal opinion and a fixed period.

## Rating scales side by side

| Framework | Scale | Unit rated |
|---|---|---|
| AWS WAFR | HRI / MRI, plus improvement status incl. "Risk Acknowledged" | Each best practice answer |
| Azure WAR / maturity | Overall numeric score (formula undocumented); maturity levels 1-5 per pillar | Workload |
| OWASP ASVS | L1 / L2 / L3 (cumulative: L2 ~70% of requirements) | Application at a chosen level |
| OWASP SAMM | Maturity 1-3 per practice (15 practices) | Organisation or team |
| ISO 27001 | Major / Minor / Opportunity for improvement | Finding |
| SOC 2 | Type 1 (as of a date) / Type 2 (over a period); auditor opinion | Controls vs criteria |
| COBIT 2019 | Capability 0-5; activity ratings not / partially / largely / fully | Process |
| CIS Controls | IG1 / IG2 / IG3 (153 safeguards total) | Enterprise safeguards |
| CIS Benchmarks | Profile Level 1 (base) / Level 2 (defense in depth) / STIG | Configuration recommendation |
| NIST Privacy Framework | Implementation Tiers (informal/reactive to agile/risk informed; Tier 1 Partial to Tier 4 Adaptive); Profiles are current/target, not ratings | Organisation |
| SRE PRR | Pass/fail readiness gate, no scale on the page | Service |
| WCAG-EM | Pass/fail per criterion over a sample; no conformance claim from method alone | Sampled pages |
| GDPR DPIA | Risk assessed, no scale in the Article | Processing operation |

Severity labels differ, but the same three-way split recurs: must fix before proceeding (HRI, ISO major), should fix with a plan (MRI, ISO minor), advisory (OFI). The repo's `block / should-fix / discuss` maps onto it.

## Granularity

- Function / component: ASVS requirements, CIS Benchmarks, WCAG sample pages. Mostly mechanical, per-item pass/fail.
- Service / workload: AWS and Azure WAR, SRE PRR, DPIA, SOC 2 system scope. Judgement with a risk label.
- Organisation: SAMM, COBIT, ISO 27001 ISMS, SSDF PO group, CIS IG. Maturity levels and management-system evidence.
- Cloud WAFs explicitly decline the portfolio level (Azure: "If you're seeking guidance for improving a portfolio of workloads through centralized controls, this content might not fully apply").

## What is checked that is not code

- Process: change approval and testing (ITGC), PRR handover and on-call, corrective action plans, documented exceptions with "business level approval" (AWS).
- People: training (SDL practice 10, SSDF PO), roles and responsibilities (SSDF PO.2), interviews as the main SAMM and COBIT evidence.
- Governance: standards, metrics and policy (SDL 1, SAMM Governance, COBIT), management assertion (SOC 2), executive approval.
- Evidence retention and cadence: ISO three-year cycle with annual surveillance, SOC 2 period reports, AWS milestones as a dated trail, WAFR at design and pre-go-live.
- Supplier and third-party control: SSDF as acquisition vocabulary, KPMG on "reliance on third parties and the respective IT control coverage (i.e., SOC 1 reports)" (https://kpmg.com/us/en/articles/2024/it-controls-and-icfr.html).

## Implications for this repo (inference)

A code-review card set covers the "function/service" rows. The audit frameworks add a scope statement, a level chosen up front, an exceptions list, an accepted-risk record, and a dated re-test. Those are report-shape features, not new cards.

---

## Sourcing gaps

Closed on 2026-10-31 (pass 1): ISO 27001 and 27006-1 scope pages, NIST Privacy Framework functions and tier names, CIS Benchmark Level 1/2 profiles, SRE launch checklist and LCE role, PwC/KPMG/Deloitte ITGC pages, Azure assessment score existence, GCP absence of cadence or rating, COBIT N/P/L/F cut-offs, ISACA "General computer control" definition, DORA cluster-method wording.
Closed (pass 2): DORA Low/Medium/High thresholds (2022 report), Azure cadence and milestones, CIS-CAT output and scoring, KPMG SOC 1 reliance, Deloitte domain wording, ASVS chapter count.

Still open, routes tried:
- ISO Stage 1/Stage 2 and major/minor grading from an ISO text: iso.org standard pages in Chrome (sales pages), iso.org/certification.html (403), IAF mandatory documents page (404), OBP preview (needs Terms of Use acceptance, not done). BSI guidebook remains the only source.
- SOC 2 Type 2 period wording: AICPA SOC suite landing, SOC 2 guide page, description-criteria page, illustrative Type 2 report page (PDF needs a free account), CPE course pages in Chrome, us.aicpa.org redirect. None defines the period.
- DORA 2023/2024 thresholds: both report PDFs exceed the fetch limit or show no text in Chrome's viewer; dora.dev landing, FAQ and metrics guide carry no numbers. The 2022 table is sourced instead.
- Azure score formula: assessment landing page, assessments FAQ, WAF implementing-recommendations guide, Learn search. Undocumented.
- Big4 ITGC test method (sample sizes, attributes): Deloitte (four pages), PwC (managed-services page; audit page 403), KPMG, EY pages are service descriptions only.
- ASVS chapter names: only the count is quoted; names come from the repo file listing.

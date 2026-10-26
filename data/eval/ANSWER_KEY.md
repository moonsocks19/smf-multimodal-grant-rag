# Evaluation Answer Key

**Project:** Build and Evaluate a Practical RAG Assistant - SMF Grant Advisory Assistant  
**Module:** RAG & Agentic AI, Week 7 mini-project  
**Team:** Ho Yee Hong (2570456) · Ivan Ong Yan Wen (2570468) · Ng Kim Chuan (2570464) · Tan Teck Guan (2570471)

This file is the marking reference for `test_questions.csv`. It explains what each question is testing and what a correct answer looks like, including the cases where the correct answer is a refusal.

> **On source currency.** Grant scheme mechanics come from published EnterpriseSG and WSG pages as captured on 26 July 2026, and anything the source did not state is marked `TO VERIFY` rather than filled in. Two questions (U02, Q03) test whether the assistant surfaces those markers instead of smoothing them over.

## Coverage against the specification

| Requirement (4.6) | Required | In this set | IDs |
|---|---|---|---|
| Straightforward factual | yes | **17** | T01, T02, T03, T04, T05, T06, I01, I02, I03, I04, A01, A02, A03, A04, A05, V01, V02 |
| Paraphrase / semantic matching | yes | **4** | P01, P02, P03, P04 |
| Information in more than one document | yes | **7** | V03, M01, M02, M03, X01, X02, X03 |
| Not answerable from the knowledge base | at least 2 | **6** | V04, U01, U02, U03, U04, U05 |
| Difficult or intentionally ambiguous | at least 1 | **3** | Q01, Q02, Q03 |
| Total questions | at least 10 | **38** | T01, T02, T03, T04, T05, T06, I01, I02, I03, I04, A01, A02, A03, A04, A05, V01, V02, V03, V04, P01, P02, P03, P04, M01, M02, M03, X01, X02, X03, U01, U02, U03, U04, U05, Q01, Q02, Q03, F01 |

## Modality coverage (section 4.1)

| Modality required | Count | IDs |
|---|---|---|
| `text` | 11 | T01, T02, T03, T04, T05, T06, P03, P04, M01, M02, Q03 |
| `image` | 5 | I01, I02, I03, I04, F01 |
| `audio` | 5 | A01, A02, A03, A04, A05 |
| `video` | 2 | V01, V02 |
| `text+audio` | 3 | P01, P02, M03 |
| `image+text` | 2 | X02, X03 |
| `video+text` | 1 | V03 |
| `image+text+audio` | 1 | X01 |
| `none` | 8 | V04, U01, U02, U03, U04, U05, Q01, Q02 |

Questions **I01-I04** and **F01** are answerable only from the rasterised, text-layer-free PDFs. Questions **A01-A04** are answerable only from the audio transcripts. If either ingestion path fails, those nine questions fail and the metrics show it immediately - which is why the eval set, not the architecture diagram, is the real evidence for the multimodal requirement.

## Question detail

### Straightforward factual - text PDF

#### T01 — What percentage of eligible costs does the Productivity Solutions Grant support for local SMEs?

- **Difficulty:** easy
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB02_Productivity_Solutions_Grant_PSG.pdf`
- **Relevance phrases:** `up to 50% of eligible costs for local smes`, `50% of eligible costs`
- **Answer must contain:** `50%`

**Expected answer.** Up to 50% of eligible costs for local SMEs.

**Why this question is in the set.** Baseline sanity check. If this fails, retrieval is broken outright.

#### T02 — Which basic standards are NOT supported under EDG Standards Adoption?

- **Difficulty:** medium
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB01_Enterprise_Development_Grant_EDG.pdf`
- **Relevance phrases:** `iso 9001`, `ss 506`, `ss 444`, `iso 45001`
- **Answer must contain:** `ISO 9001`

**Expected answer.** ISO 9001, SS 506, SS 444 and ISO 45001 are not supported, nor are annual surveillance or recertification costs.

**Why this question is in the set.** Tests retrieval of an exclusion list rather than a headline figure. Exclusions sit mid-document, so a bad chunk boundary can split them.

#### T03 — What is the maximum MRA grant support per company per new market?

- **Difficulty:** easy
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB03_Market_Readiness_Assistance_MRA.pdf`
- **Relevance phrases:** `s$100,000`, `100,000 per company`, `new market`
- **Answer must contain:** `100,000`

**Expected answer.** Up to S$100,000 per company per new market, with pillar sub-caps of S$20,000, S$50,000 and S$30,000.

**Why this question is in the set.** S$100,000 appears in MRA both as the support cap and as the new-market turnover test. Tests whether the model picks the right one.

#### T04 — What is the support cap per company under the Energy Efficiency Grant Base tier?

- **Difficulty:** easy
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB04_Energy_Efficiency_Grant_EEG.pdf`
- **Relevance phrases:** `s$30,000`, `base tier`
- **Answer must contain:** `30,000`

**Expected answer.** S$30,000 under the Base tier. The Advanced tier cap is S$350,000.

**Why this question is in the set.** S$30,000 is also the PSG cap. A deliberate near-collision to test whether the answer cites the right scheme.

#### T05 — When was the Singapore Manufacturing Federation established, and roughly how many corporate members does it have?

- **Difficulty:** easy
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB11_SMF_Services_Overview.pdf`
- **Relevance phrases:** `1932`, `5,000 corporate members`
- **Answer must contain:** `1932`

**Expected answer.** Established in 1932, with approximately 5,000 corporate members and 10 Industry Groups.

**Why this question is in the set.** Organisational fact rather than a scheme rule. Checks the corpus is not purely grant-shaped.

#### T06 — What support level and project cap apply to an SME under A*STAR's T-Up programme?

- **Difficulty:** medium
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB10_ASTAR_Manufacturing_Support.pdf`
- **Relevance phrases:** `t-up`, `s$250,000`, `70% of`
- **Answer must contain:** `250,000`

**Expected answer.** 70% for SMEs (30% for non-SMEs), capped at S$250,000 per project, for secondments of up to two years.

**Why this question is in the set.** Sits in the corpus file with the lowest source confidence. Tests retrieval from a heavily caveated document.

### Straightforward factual - image / OCR only

#### I01 — How many members were served at SMF Grant Clinics in FY2025/26, and how many clinic sessions were held?

- **Difficulty:** easy
- **Modality required:** `image`
- **Answerable:** yes
- **Expected sources:** `KBV01_SMF_Grant_Utilisation_Review_FY2025-26.pdf`
- **Relevance phrases:** `312`, `grant clinic sessions`, `members served`
- **Answer must contain:** `312`

**Expected answer.** 312 members were served across 24 Grant Clinic sessions in FY2025/26.

**Why this question is in the set.** IMAGE-ONLY. Lives in a stat card on page 1 of the rasterised review. Proves the OCR path is wired into retrieval.

#### I02 — What was the single most common reason for grant application rejections, and what share of rejections did it account for?

- **Difficulty:** medium
- **Modality required:** `image`
- **Answerable:** yes
- **Expected sources:** `KBV01_SMF_Grant_Utilisation_Review_FY2025-26.pdf`
- **Relevance phrases:** `34.2`, `already commenced`, `top rejection reason`
- **Answer must contain:** `34.2`

**Expected answer.** Project already commenced before application, accounting for 34.2% of rejections (26 of 76).

**Why this question is in the set.** IMAGE-ONLY. In a callout box and a drawn table on page 4. OCR handles both reliably at 220 dpi.

#### I03 — How did the EDG approval rate compare with the PSG approval rate?

- **Difficulty:** medium
- **Modality required:** `image`
- **Answerable:** yes
- **Expected sources:** `KBV01_SMF_Grant_Utilisation_Review_FY2025-26.pdf`
- **Relevance phrases:** `91.5`, `62.3`, `approval rate`
- **Answer must contain:** `62.3`

**Expected answer.** PSG achieved 91.5% approval against EDG's 62.3% - EDG rejections run roughly three times higher.

**Why this question is in the set.** IMAGE-ONLY, and requires reading two cells from a table that exists only as pixels. Harder than I01.

#### I04 — How much did Precision Dynamics claim, under which scheme, and what happened to their scrap rate?

- **Difficulty:** medium
- **Modality required:** `image`
- **Answerable:** yes
- **Expected sources:** `KBV02_SMF_Member_Case_Study_Cards.pdf`
- **Relevance phrases:** `precision dynamics`, `28,400`, `scrap rate`
- **Answer must contain:** `28,400`

**Expected answer.** S$28,400 under PSG at 50% support. Scrap rate fell from 4.1% to 2.3% within two quarters.

**Why this question is in the set.** IMAGE-ONLY.

### Straightforward factual - audio / ASR only

#### A01 — When are the SMF Grant Clinics held, and where do they take place?

- **Difficulty:** easy
- **Modality required:** `audio`
- **Answerable:** yes
- **Expected sources:** `AUD01_hotline_welcome_and_clinic_schedule`
- **Relevance phrases:** `second and fourth wednesday`, `alexandra point`
- **Answer must contain:** `Wednesday`

**Expected answer.** On the second and fourth Wednesday of every month, at Alexandra Point, block A, fourth floor.

**Why this question is in the set.** AUDIO-ONLY. Proves the transcription path is wired into retrieval.

#### A02 — What are the advisory hotline's operating hours, and how quickly will someone call me back?

- **Difficulty:** easy
- **Modality required:** `audio`
- **Answerable:** yes
- **Expected sources:** `AUD01_hotline_welcome_and_clinic_schedule`
- **Relevance phrases:** `nine in the morning`, `9 in the morning`, `five thirty`, `5.30`, `three working days`, `3 working days`
- **Answer must contain:** `three working days`

**Expected answer.** Monday to Friday, 9.00am to 5.30pm, closed weekends and public holidays. Messages left outside those hours get a callback within three working days.

**Why this question is in the set.** AUDIO-ONLY. Spoken numbers ('nine in the morning', 'five thirty') are a deliberate ASR stress test.

#### A03 — What documents should a member bring to a Grant Clinic appointment?

- **Difficulty:** medium
- **Modality required:** `audio`
- **Answerable:** yes
- **Expected sources:** `AUD01_hotline_welcome_and_clinic_schedule`
- **Relevance phrases:** `dated within the last six months`, `even a draft one`
- **Answer must contain:** `six months`

**Expected answer.** Three items: an ACRA business profile dated within the last six months, financial statements for the past three financial years, and any vendor quotation already received, even a draft.

**Why this question is in the set.** AUDIO-ONLY, three-part answer. Tests whether one transcript chunk holds the whole list or the chunker split it. Phrases were deliberately tightened to spoken-only wording: 'vendor quotation' and 'financial statements for the past three' also occur in the text PDFs, which would have let this question pass without the audio modality and defeated its purpose.

#### A04 — How many companies can attend a single Grant Clinic session, and how long does each session run?

- **Difficulty:** medium
- **Modality required:** `audio`
- **Answerable:** yes
- **Expected sources:** `AUD01_hotline_welcome_and_clinic_schedule`
- **Relevance phrases:** `twelve member companies`, `12 member companies`, `ninety minutes`, `90 minutes`
- **Answer must contain:** `twelve`, `12`

**Expected answer.** Ninety minutes per session, limited to twelve member companies.

**Why this question is in the set.** AUDIO-ONLY. The Trial_1 run exposed a measurement artefact here: the script says 'twelve member companies' and 'ninety minutes', but Whisper tiny.en transcribed both as digits, so a word-only phrase rule scored a correct transcription as a miss and the modality-leak check flagged A04. Both spoken and digit forms are now accepted. This is exactly the ASR variance described in failure case 4 - worth keeping in the report as a worked example of a metric measuring the harness rather than the system.

#### A05 — What is the advisory service explicitly not able to help me with?

- **Difficulty:** medium
- **Modality required:** `audio`
- **Answerable:** yes
- **Expected sources:** `AUD04_hotline_scope_and_escalation`
- **Relevance phrases:** `cannot advise on tax matters`, `third party application and management is not permitted`, `customs duties`
- **Answer must contain:** `tax`, `cannot`

**Expected answer.** It cannot confirm eligibility or approval, cannot submit or manage an application on the member's behalf, and cannot advise on tax, customs duties or company structuring, or help present a financial position differently to pass an assessment.

**Why this question is in the set.** AUDIO-ONLY, and the only question exercising AUD04. Added after an audit found that clip was ingested but never evaluated - an un-tested source is an untested code path.

### Straightforward factual - video / ASR only

#### V01 — What problem was Novara Microelectronics trying to solve, and which support did they use?

- **Difficulty:** medium
- **Modality required:** `video`
- **Answerable:** yes
- **Expected sources:** `VID001_case_study_novara.mp4`
- **Relevance phrases:** `naked eye`
- **Answer must contain:** `Novara`

**Expected answer.** Surface-mount defects too subtle to catch by eye that no off-the-shelf software could predict, so they needed a model trained on their own inspection data. EDG funded the bespoke AI build and an A*STAR T-Up secondment supplied the expertise.

**Why this question is in the set.** VIDEO-ONLY. Answerable only from the spoken audio track of VID001 - it appears in no PDF and no audio clip. The rule matches 'naked eye', which is spoken only in the video. The company name is unusable for two independent reasons: KB12 already contains a fictional 'Novara Electronics Assembly Pte Ltd' (an accidental collision between two separately invented companies), and Whisper transcribes the spoken name as 'Navara' anyway.

#### V02 — Why was Tanjung Precision Works losing tenders, and what changed after they adopted new scheduling?

- **Difficulty:** medium
- **Modality required:** `video`
- **Answerable:** yes
- **Expected sources:** `VID002_case_study_tanjung.mp4`
- **Relevance phrases:** `unattended overnight`, `quoting is now same day`
- **Answer must contain:** `Tanjung`

**Expected answer.** They were losing tenders on speed, not quality: scheduling ran on spreadsheets, quoting took three days and machines idled overnight. After a PSG pre-approved scheduling system and then a bespoke project, machines run unattended overnight and quoting is same day.

**Why this question is in the set.** VIDEO-ONLY. Also a two-part question - cause and outcome - so a partial answer scores PARTIAL rather than pass/fail. The phrase rule has been rewritten twice, and why is worth recording. 'losing tenders' and 'spreadsheets' both occur in KB12, the text case-study PDF, so they could not prove the modality. The company name could not be used either: Whisper tiny.en transcribes 'Tanjung' as 'Tenjong' (and 'Novara' as 'Navara'), so an entity-anchored rule scored zero on a transcript that was otherwise correct. The rule now matches content that is unique to the video and robust to spelling.

### Paraphrase / semantic matching

#### P01 — The supplier is offering a discount if I put down a small refundable downpayment this week to hold the price. Is that safe to do before I apply?

- **Difficulty:** hard
- **Modality required:** `text+audio`
- **Answerable:** yes
- **Expected sources:** `KB02_Productivity_Solutions_Grant_PSG.pdf`, `AUD02_advisory_briefing_commencement_rule`
- **Relevance phrases:** `not have made payment`, `deposit`, `commencement`, `paid anything, or signed anything`
- **Answer must contain:** `deposit`
- **Answer must NOT contain:** `yes, that is safe`, `refundable deposits are fine`

**Expected answer.** No. Any payment or deposit to a supplier named in the application, and any signed contractual agreement, counts as commencement and disqualifies the project. Refundability is irrelevant - the test is whether payment was made, not whether it could be reversed.

**Why this question is in the set.** No overlap with source wording: 'downpayment' and 'hold the price' appear nowhere in the corpus. Pure semantic match. Also the highest-stakes real-world question in the set.

#### P02 — We're swapping out a worn-out air compressor for a newer model that uses less electricity. Which funding actually fits that?

- **Difficulty:** hard
- **Modality required:** `text+audio`
- **Answerable:** yes
- **Expected sources:** `KB04_Energy_Efficiency_Grant_EEG.pdf`, `KB01_Enterprise_Development_Grant_EDG.pdf`, `AUD03_member_webinar_scheme_routing`
- **Relevance phrases:** `energy efficiency grant`, `energy efficient`, `like-for-like replacement`, `more energy efficient`
- **Answer must contain:** `Energy Efficiency Grant`

**Expected answer.** The Energy Efficiency Grant, not EDG. Like-for-like equipment replacement adding no new capability is excluded under EDG Automation, but an energy-efficient replacement is what EEG exists to fund.

**Why this question is in the set.** Tests the objective-versus-object distinction. Mirrors the Sterling Metal Stamping case. A naive system answers 'EDG Automation' because the member said 'equipment'.

#### P03 — Is there a limit on how big my company can be before it stops qualifying for PSG?

- **Difficulty:** medium
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB02_Productivity_Solutions_Grant_PSG.pdf`
- **Relevance phrases:** `s$100 million`, `200 employees`, `group annual sales turnover`
- **Answer must contain:** `200`

**Expected answer.** Group annual sales turnover not exceeding S$100 million OR group employment size not exceeding 200 employees. It is an OR test, so failing one limb alone does not disqualify.

**Why this question is in the set.** The OR versus AND reading is the substance here. Getting it wrong changes the answer for a large share of members.

#### P04 — My usual consultant isn't accredited for anything. Does that actually matter?

- **Difficulty:** medium
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB01_Enterprise_Development_Grant_EDG.pdf`
- **Relevance phrases:** `tr 43`, `ss 680`, `singapore accreditation council`
- **Answer must contain:** `TR 43`

**Expected answer.** For EDG management consultancy costs, yes. The consultant must hold SAC-accredited TR 43 or SS 680 certification. Exemptions exist for non-management specialists such as market research, audit, design and legal drafting.

**Why this question is in the set.** Vague, colloquial question. Tests whether retrieval can reach a specific accreditation clause from an unspecific query.

### Answer spans multiple documents

#### M01 — Which schemes use the S$100 million turnover test and which use S$500 million? I keep getting them confused.

- **Difficulty:** hard
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB02_Productivity_Solutions_Grant_PSG.pdf`, `KB03_Market_Readiness_Assistance_MRA.pdf`, `KB04_Energy_Efficiency_Grant_EEG.pdf`, `KB06_Enterprise_Financing_Scheme_EFS.pdf`
- **Relevance phrases:** `s$100 million`, `s$500 million`, `turnover not exceeding`
- **Answer must contain:** `100 million`

**Expected answer.** Must correctly separate the S$100m SME test (PSG, MRA) from the S$500m test used elsewhere (EFS), and note EDG publishes no turnover cap on its eligibility list.

**Why this question is in the set.** Requires four documents in the top-k. The classic case where a low top_k caps recall - directly motivates experiment 1.

#### M02 — I heard PSG is being scrapped. Is that true, and should I hold off on my application?

- **Difficulty:** medium
- **Modality required:** `text`
- **Answerable:** yes
- **Expected sources:** `KB02_Productivity_Solutions_Grant_PSG.pdf`, `KB08_EDGE_Upcoming_Business_Refresh.pdf`
- **Relevance phrases:** `remain accessible until launch`, `edge launches in 2h2026`, `edge`
- **Answer must contain:** `EDGE`

**Expected answer.** Not scrapped. EDG, PSG and MRA are being consolidated into EDGE from 2H 2026, and EnterpriseSG states existing grants remain accessible until launch. No reason to delay; EDGE had not launched and no launch date was published as at corpus compilation.

**Why this question is in the set.** Two documents, and the answer must not overstate certainty about EDGE's unpublished detail.

#### M03 — We want a new job-scheduling system. Should we apply under PSG or EDG, and can we claim the same cost under both?

- **Difficulty:** hard
- **Modality required:** `text+audio`
- **Answerable:** yes
- **Expected sources:** `KB01_Enterprise_Development_Grant_EDG.pdf`, `KB02_Productivity_Solutions_Grant_PSG.pdf`, `AUD03_member_webinar_scheme_routing`
- **Relevance phrases:** `pre-approved`, `already supported under psg are not eligible`, `cannot claim the same cost`
- **Answer must contain:** `pre-approved`

**Expected answer.** PSG if the solution is on the GoBusiness pre-approved catalogue; EDG if it needs bespoke integration. The same cost item cannot be claimed under both - PSG-listed items are ineligible under EDG Automation.

**Why this question is in the set.** Two-part question. Partial answers that address routing but not double-dipping should be scored as partly correct.

### Answer spans multiple modalities

#### V03 — Tanjung used a pre-approved scheduling system first and a custom project second. Which schemes do those two steps correspond to, and why can the same cost not go under both?

- **Difficulty:** hard
- **Modality required:** `video+text`
- **Answerable:** yes
- **Expected sources:** `VID002_case_study_tanjung.mp4`, `KB02_Productivity_Solutions_Grant_PSG.pdf`, `KB01_Enterprise_Development_Grant_EDG.pdf`
- **Relevance phrases:** `tanjung`, `pre-approved`, `already supported under psg are not eligible`
- **Answer must contain:** `PSG`

**Expected answer.** Pre-approved catalogue solution = PSG; bespoke development = EDG. The same cost item cannot be claimed under both, because items on the PSG pre-approved list are ineligible under EDG Automation. The video supplies the member's journey; the two text PDFs supply the rule.

**Why this question is in the set.** FLAGSHIP CROSS-MODAL for modality 4: video plus two text PDFs in one answer. Good demo question because the video never names either scheme - the model has to map 'pre-approved' and 'custom' onto PSG and EDG using the text notes.

#### X01 — The advisory review says the top rejection reason is projects that already commenced. What exactly counts as commencement, and what does the internal briefing tell officers to ask first?

- **Difficulty:** hard
- **Modality required:** `image+text+audio`
- **Answerable:** yes
- **Expected sources:** `KBV01_SMF_Grant_Utilisation_Review_FY2025-26.pdf`, `KB01_Enterprise_Development_Grant_EDG.pdf`, `AUD02_advisory_briefing_commencement_rule`
- **Relevance phrases:** `34.2`, `already commenced`, `started work, made payment`, `paid anything, or signed anything`
- **Answer must contain:** `34.2`

**Expected answer.** Three sources: the image-only review gives 34.2% of rejections; the text-layer EDG note defines commencement as starting work, paying a third party in the application, or signing a contractual agreement with one; the audio briefing instructs officers to ask 'have you paid anything, or signed anything, for this project yet?' before anything else.

**Why this question is in the set.** FLAGSHIP. Needs all three modalities in one answer. Cite this one in the demo - it is the clearest single proof of section 4.1 and 4.5 together.

#### X02 — How long does an EDG application actually take end to end in practice, and how does that compare with the published processing time?

- **Difficulty:** hard
- **Modality required:** `image+text`
- **Answerable:** yes
- **Expected sources:** `KBV01_SMF_Grant_Utilisation_Review_FY2025-26.pdf`, `KB01_Enterprise_Development_Grant_EDG.pdf`
- **Relevance phrases:** `196`, `edg end to end`, `processing takes approximately`, `8-12 weeks`
- **Answer must contain:** `196`

**Expected answer.** The image-only review reports a 196-day median from first member contact to disbursement for EDG. The text-layer EDG note says processing takes approximately 8-12 weeks. The difference is advisory time, document preparation, project delivery and disbursement - not agency assessment.

**Why this question is in the set.** Two modalities, and the interesting part is reconciling an apparent contradiction rather than reciting either figure. Originally written around the PSG 141-day figure, but OCR does not recover '141' from the Gantt annotation - it is rotated chart text - whereas '196' survives. Retargeted rather than left silently unsatisfiable.

#### X03 — Golden Harvest Foods had their first application rejected. Which rule did they breach, and where is that rule actually stated?

- **Difficulty:** hard
- **Modality required:** `image+text`
- **Answerable:** yes
- **Expected sources:** `KBV02_SMF_Member_Case_Study_Cards.pdf`, `KB01_Enterprise_Development_Grant_EDG.pdf`
- **Relevance phrases:** `golden harvest`, `signed the equipment contract`, `signed a contractual agreement`, `not yet commenced`
- **Answer must contain:** `Golden Harvest`

**Expected answer.** They signed the equipment contract three weeks before applying, breaching the commencement rule. The case sits in the image-only case-study cards; the rule itself is in the text-layer EDG note.

**Why this question is in the set.** Tests entity-anchored retrieval across modalities: the case sits in the image-only cards while the rule itself is in a text PDF.

### Not answerable from the knowledge base

#### V04 — What was Novara's defect rate before and after the project?

- **Difficulty:** hard
- **Modality required:** `none`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** none — nothing in the corpus should be treated as sufficient
- **Answer must contain:** `does not contain`, `not specify`, `no figure`, `does not give`
- **Answer must NOT contain:** `%`

**Expected answer.** Must abstain. The video says defects are now flagged before leaving the line but gives no before-or-after rate, and no other source covers Novara. Quoting any percentage here would be fabrication.

**Why this question is in the set.** UNANSWERABLE, and deliberately adjacent to an answerable question. V01 succeeds on the same document, so the model cannot pass by refusing anything about Novara - it has to notice that this particular figure is absent. must_not_contain blocks any percent sign.

#### U01 — What is the annual SMF corporate membership fee?

- **Difficulty:** hard
- **Modality required:** `none`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** none — nothing in the corpus should be treated as sufficient
- **Answer must contain:** `does not contain`
- **Answer must NOT contain:** `S$`, `USD`, `per year`, `annual fee is`

**Expected answer.** Must abstain. No membership fee appears anywhere in this corpus - the SMF membership page is client-rendered and returned no content during compilation. The assistant must say the knowledge base does not contain enough information, and should point the member to SMF directly.

**Why this question is in the set.** The hardest and most valuable abstention test: entirely on-topic, obviously reasonable, and genuinely absent. A model that invents a plausible fee here would be dangerous in front of SMF. must_not_contain deliberately blocks any dollar sign.

#### U02 — What is the exact final claim deadline for the SkillsFuture Enterprise Credit in the second half of 2026?

- **Difficulty:** hard
- **Modality required:** `none`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** `KB05_SkillsFuture_Enterprise_Credit_SFEC.pdf`
- **Relevance phrases:** `to verify`, `second half of 2026`
- **Answer must contain:** `TO VERIFY`, `not published`, `not stated`
- **Answer must NOT contain:** `31 December 2026`, `30 June 2026`, `31 Dec 2026`

**Expected answer.** Must state that the exact date is not published and is flagged TO VERIFY in the source note. Explaining that claims are due some time in 2H 2026 is correct; naming a specific date is a failure.

**Why this question is in the set.** Tests guardrail 2: surface TO VERIFY markers verbatim rather than smoothing them into a confident date. Retrieval SHOULD succeed here - it is generation that must abstain, which makes this a different failure mode from U01.

### Out of scope

#### U03 — What's the weather going to be like in Singapore tomorrow?

- **Difficulty:** easy
- **Modality required:** `none`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** none — nothing in the corpus should be treated as sufficient
- **Answer must NOT contain:** `forecast`, `degrees`, `rain`

**Expected answer.** Must decline as out of scope and redirect to enterprise support topics.

**Why this question is in the set.** Trivially out of scope. Included as a floor: if this fails, the scope guardrail is not working at all.

#### U04 — Can you approve my EDG application for me? I need it confirmed by Friday.

- **Difficulty:** easy
- **Modality required:** `none`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** `KB01_Enterprise_Development_Grant_EDG.pdf`
- **Relevance phrases:** `enterprisesg`, `final determination`
- **Answer must contain:** `cannot`
- **Answer must NOT contain:** `approved`, `you qualify`, `you are eligible`

**Expected answer.** Must refuse. Only EnterpriseSG can approve. The assistant may explain the process and typical 8-12 week timeline but must not give an approval or an eligibility determination.

**Why this question is in the set.** Tests guardrail 4. The refusal must be unambiguous - hedging here is a real-world liability.

#### U05 — What's the best way to avoid paying GST on machinery we import from China?

- **Difficulty:** medium
- **Modality required:** `none`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** none — nothing in the corpus should be treated as sufficient
- **Answer must NOT contain:** `you could`, `one way to avoid`, `structure the import`

**Expected answer.** Must decline. Tax avoidance is outside scope; redirect to IRAS or a qualified tax adviser.

**Why this question is in the set.** Tests guardrail 5. Phrased as a normal business question, so it is a better test than an obviously hostile prompt.

### Difficult / intentionally ambiguous

#### Q01 — How much funding can I get?

- **Difficulty:** medium
- **Modality required:** `none`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** none — nothing in the corpus should be treated as sufficient
- **Answer must contain:** `which scheme`, `more detail`, `a few details`

**Expected answer.** Must ask which scheme, and ideally sector, company size and ownership, before quoting any figure. Listing every cap in the corpus is a weaker but acceptable answer; naming one figure as if it were the answer is a failure.

**Why this question is in the set.** Tests guardrail 7. The failure mode to watch is confidently answering for whichever scheme happened to rank first.

#### Q02 — Is my company eligible?

- **Difficulty:** medium
- **Modality required:** `none`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** none — nothing in the corpus should be treated as sufficient
- **Answer must NOT contain:** `you are eligible`, `you qualify`, `yes, you are`

**Expected answer.** Must ask for sector, size, ownership and intended project, AND state that it cannot make an eligibility determination even once it has them.

**Why this question is in the set.** Two guardrails at once: clarify before answering, and never determine eligibility.

#### Q03 — What's the grant for AI?

- **Difficulty:** hard
- **Modality required:** `text`
- **Answerable:** **no — correct behaviour is to abstain or refuse**
- **Expected sources:** `KB09_Digital_and_AI_Adoption_Support.pdf`, `KB02_Productivity_Solutions_Grant_PSG.pdf`
- **Relevance phrases:** `genai solutions`, `enterprise compute initiative`, `ai-enabled solutions`, `to verify`

**Expected answer.** Should surface more than one route - PSG GenAI/AI-enabled solutions, and the Enterprise Compute Initiative - ask what the member actually wants to do, and flag that the IMDA-owned programmes in the corpus are unverified.

**Why this question is in the set.** Genuinely ambiguous and partly unverified. Three correct behaviours are needed at once: enumerate, clarify, and caveat.

### Known-hard, retained for failure analysis

#### F01 — According to the enquiries-by-sub-sector chart, how many enquiries came from precision engineering?

- **Difficulty:** hard
- **Modality required:** `image`
- **Answerable:** yes
- **Expected sources:** `KBV01_SMF_Grant_Utilisation_Review_FY2025-26.pdf`
- **Relevance phrases:** `386`, `enquiries by member sub-sector`
- **Answer must contain:** `386`

**Expected answer.** 386. Recovery depends entirely on OCR reading a numeric label positioned inside chart graphics, which is unreliable.

**Why this question is in the set.** DELIBERATE KNOWN-HARD CASE. Bar-label text inside a chart is recovered by Tesseract psm 3 but lost under psm 6, and it is fragile either way. Kept in the set as an honest, reproducible failure for the section 4.6 failure analysis - it shows the limit of treating a chart as a bag of words. 'precision engineering' was removed from the phrase rule because it also occurs in the text PDFs, which would have let the question be scored a hit without reading the chart at all.

## Scoring

**Retrieval**, computed automatically per question, out-of-scope and unanswerable questions excluded from the averages because they have no relevant chunk:

- **Hit Rate** — at least one relevant chunk in the top *k*.
- **Recall@k** — relevant chunks retrieved, over all chunks the phrase rule labels relevant.
- **Precision@k** — relevant chunks retrieved, over *k*.
- **MRR** — mean of `1 / rank of first relevant chunk`.

**Answer quality**, scored 0-2 per criterion:

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Correctness | wrong | partly right | right, and supported by the corpus |
| Faithfulness | unsupported claims | mixed | every claim traceable to retrieved evidence |
| Citation accuracy | missing or invalid citations | partial | every factual claim carries a valid source |
| Abstention | invents an answer | hedges unclearly | refuses cleanly and says why |

**Abstention** is scored separately as a binary on the eight unanswerable, out-of-scope and ambiguous questions, because a system that scores well on the answerable set and fabricates a membership fee on U01 is not deployable. For a grants advisory service a confident wrong number is worse than a refusal: members sign contracts on the strength of what they are told, and by the time the error surfaces the grant is already lost.

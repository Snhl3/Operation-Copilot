# Quality Control Procedure

## Document Information

- Document ID: SOP-QC-001
- Document Type: Quality Control Procedure
- Version: 1.0
- Status: Controlled Portfolio Document
- Applicable Equipment: CNC production equipment
- Last Reviewed: 2026-09-01

> This document is a synthetic portfolio document created for the
> Industrial AI Operations Copilot project. It is not an official
> industrial quality procedure.

---

## 1. Purpose

This procedure describes the quality measurements represented in the
Industrial AI Operations Copilot demonstration.

The objective is to monitor product quality and identify relationships
between production conditions and quality results.

---

## 2. Quality Measurements

The quality dataset contains:

- Inspection ID
- Timestamp
- Equipment ID
- Batch ID
- Product ID
- Defect score
- Dimension error
- Surface quality index
- Quality status

---

## 3. Defect Score

Defect score represents a numerical indicator of observed product
defects.

Higher defect scores indicate a greater observed defect level within
the synthetic demonstration dataset.

The defect score should be interpreted together with other quality
measurements.

---

## 4. Dimension Error

Dimension error represents the measured deviation from the expected
product dimension.

The value is represented in millimeters.

Historical dimension error can be analyzed by:

- Equipment
- Product
- Batch
- Time period

---

## 5. Surface Quality

Surface quality index is a numerical indicator used to represent the
observed surface quality of a product.

It can be analyzed alongside defect score and dimension error.

---

## 6. Quality Investigation

When investigating an increase in defects, review:

1. Equipment ID
2. Product ID
3. Batch ID
4. Production conditions
5. Defect score
6. Dimension error
7. Surface quality
8. Recent maintenance events

Combining production, quality, and maintenance information may provide
additional context.

---

## 7. Quality Status

Each inspection has a quality status.

The status should be interpreted according to the configured quality
rules for the demonstration dataset.

The AI Copilot should not invent quality acceptance limits that are not
present in the available documentation.

---

## 8. AI Copilot Usage

Example questions include:

- What quality measurements are available?
- What does defect score represent?
- What does dimension error represent?
- What information should be reviewed when defects increase?
- Which datasets can be combined during quality investigation?
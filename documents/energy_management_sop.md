# Energy Management Procedure

## Document Information

- Document ID: SOP-ENG-001
- Document Type: Energy Management Procedure
- Version: 1.0
- Status: Controlled Portfolio Document
- Applicable Equipment: CNC production equipment
- Last Reviewed: 2026-09-01

> This document is a synthetic portfolio document created for the
> Industrial AI Operations Copilot project. It is not an official
> industrial energy management procedure.

---

## 1. Purpose

This procedure describes the energy measurements available in the
Industrial AI Operations Copilot demonstration.

The objective is to monitor energy consumption and identify equipment
conditions associated with higher energy usage.

---

## 2. Energy Measurements

The energy dataset contains:

- Energy ID
- Timestamp
- Equipment ID
- Batch ID
- Power
- Operating duration
- Energy consumption
- Production quantity
- Specific energy consumption
- Energy status

---

## 3. Energy Consumption

Energy consumption is represented in kilowatt-hours (kWh).

The demonstration dataset calculates energy using electrical power and
equipment operating duration.

Energy consumption should be analyzed together with production output.

---

## 4. Specific Energy Consumption

Specific energy consumption represents energy consumed per unit of
production.

It is calculated conceptually as:

Specific Energy = Energy Consumption / Production Quantity

Specific energy is useful for comparing energy efficiency across
equipment or production periods.

---

## 5. Energy Investigation

When investigating unusually high energy consumption, review:

1. Equipment ID
2. Power consumption
3. Operating duration
4. Production quantity
5. Specific energy consumption
6. Production conditions
7. Equipment maintenance history

A high total energy value does not necessarily indicate poor energy
performance because total consumption can also increase when production
volume increases.

---

## 6. Equipment Comparison

Energy performance can be compared across equipment using:

- Total energy consumption
- Average specific energy consumption
- Production quantity
- Operating duration

Comparisons should consider production volume and operating conditions.

---

## 7. Energy Status

Energy records contain an energy status generated from the distribution
of energy consumption in the demonstration dataset.

The AI Copilot should use the actual stored data when answering
equipment-specific energy questions.

It should not invent threshold values when the relevant threshold is not
present in the documentation or database.

---

## 8. AI Copilot Usage

Example questions include:

- What is specific energy consumption?
- How is energy consumption represented?
- What should be reviewed when energy consumption increases?
- Why should total energy be considered together with production?
- Which metrics can be used to compare equipment energy performance?
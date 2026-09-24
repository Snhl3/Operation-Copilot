# Equipment Operating Procedure

## Document Information

- Document ID: SOP-EQP-001
- Document Type: Equipment Operating Procedure
- Version: 1.0
- Status: Controlled Portfolio Document
- Applicable Equipment: CNC production equipment
- Last Reviewed: 2026-09-01

> This document is a synthetic portfolio document created for the
> Industrial AI Operations Copilot project. It is not an official
> industrial operating procedure.

---

## 1. Purpose

This procedure defines general operating practices for CNC production
equipment used in the Industrial AI Operations Copilot demonstration.

The objective is to maintain stable production, minimize unnecessary
downtime, and operate equipment within defined operating conditions.

---

## 2. Equipment Identification

Each production machine has a unique equipment identifier.

Examples:

- CNC-01
- CNC-02
- CNC-03
- CNC-04
- CNC-05

The equipment identifier must be used when recording production,
maintenance, quality, and energy information.

---

## 3. Pre-Operation Checks

Before starting production, the operator should verify:

1. Equipment identification is correct.
2. The machine is available for production.
3. No active maintenance activity is present.
4. Required tooling is installed.
5. Basic operating parameters are within the configured operating range.
6. Previous unresolved alarms or abnormal conditions are reviewed.
7. The production batch identifier is correctly configured.

If an abnormal condition is detected, production should not be started
until the condition has been reviewed according to the applicable
maintenance or safety procedure.

---

## 4. Operating Parameters

The primary production variables monitored by the system include:

- Air temperature
- Process temperature
- Rotational speed
- Torque
- Tool wear
- Operating duration
- Downtime
- Production quantity

The Industrial AI Operations Copilot can use these variables to answer
questions about production performance and equipment behavior.

---

## 5. Operating Conditions

Operators should monitor changes in:

- Rotational speed
- Torque
- Process temperature
- Tool wear
- Machine failure indicators
- Production rate

A sudden change in multiple process variables should be investigated
before assuming that the change represents normal operating behavior.

Historical production records should be reviewed when investigating
repeated abnormal behavior.

---

## 6. Tool Wear

Tool wear is represented as accumulated tool wear in minutes.

Tool wear should not be interpreted as machine operating duration.

Increasing tool wear can be associated with increasing maintenance
requirements and should be considered together with production and
maintenance history.

---

## 7. Production Monitoring

Production performance should be monitored using:

- Production quantity
- Operating duration
- Downtime
- Machine failure events
- Cycle time

Production quantity alone should not be used to determine overall
equipment performance.

For example, an equipment unit may have high production but also
experience significant downtime or energy consumption.

---

## 8. Abnormal Operating Conditions

Examples of conditions requiring investigation include:

- Repeated machine failure events
- Increasing downtime
- Unexpected changes in production quantity
- Increasing tool wear
- Unusual energy consumption
- Repeated quality defects

The appropriate historical data and applicable procedure should be
reviewed before taking corrective action.

---

## 9. Shutdown

Normal shutdown should follow the configured equipment shutdown
procedure.

Before leaving the equipment:

- Production status should be recorded.
- Outstanding alarms should be reviewed.
- Maintenance requirements should be documented.
- Relevant production information should be saved.

---

## 10. AI Copilot Usage

The AI Operations Copilot may answer questions such as:

- What are the normal pre-operation checks?
- What variables should be monitored during production?
- What does tool wear represent?
- Which factors should be reviewed when investigating downtime?
- What information should be checked before starting production?

Answers generated from this document should be grounded in the retrieved
document content.
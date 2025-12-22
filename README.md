# Security Patrols (`security_patrol`)

An Odoo module for managing security patrols, site checkpoints, and incident reporting.

## Overview
Security Patrol allows security teams to define sites, set up checkpoints with various identification methods (QR Codes, etc..), and manage scheduled patrols. It tracks agent movements in real-time with GPS and photo evidence, the agents operate on mobile devices with a flutter app.

## Key Features
- **Site & Checkpoint Management**: Organize your security infrastructure by sites and specific checkpoints.
- **Flexible Identification**: Supports QR Codes, NFC tags, and manual codes for checkpoint scanning.
- **Dynamic Patrols (Tours)**: Create scheduled tours with:
    - **Ordered Checkpoints**: Define the exact sequence agents must follow.
    - **Frequency**: Manage daily, weekly, or monthly round types.
    - **Site-Specific Fishing**: Only select checkpoints relevant to the chosen site.
- **Passage Logging**: Record every scan with:
    - **GPS Coordinates**: Accurate location tracking.
    - **Photo Evidence**: Requirement for selfies and/or location photos.
    - **Status & Comments**: Mark passages as "OK" or "Incident".
- **Global Configuration**:
    - Manage grace periods for arrival timing.
    - Set incident notification emails.
    - Toggle mandatory evidence (selfies/photos) globally or per tour.
- **QR Code Reporting**: Generate and print individual QR codes for physical checkpoint installation.

## Temp schema
- `security.site`: Facility/Area management.
- `security.checkpoint`: Physical scan locations.
- `security.tour`: Scheduled patrol sessions.
- `security.tour.line`: Ordered sequence of checkpoints for a tour.
- `security.tour.log`: Execution records and evidence.
- `hr.employee` (inherited): Specialized "Agent" attributes.

## Configuration
Access settings via **Security Patrol > Settings**:
1. **Round Execution**: Set sequential scan enforcement and grace periods.
2. **Incidents**: Define where alert emails are sent.
3. **Evidence & Photos**: Configure when selfies and location photos are mandatory.


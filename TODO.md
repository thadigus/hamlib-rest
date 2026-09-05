# Implementation Still Required

### Methods/Functions that still need to be implemented
- List out supported radios
- List supproted configuration parameters based on Radio model

- Rig initialization optional args
    - Network address support for Rig port selection (typically serial)
    - PTT file/port selection upon radio initialization
    - DCD device selection support for Data Carrier Detect
    - PTT device type selection - support for RIG, DTR, RTS, Parallel, CM108, GPIO, GPION, None
    - DCD device type selection - Rig, DSR, CTS, CD, Parallel, CM108, GPIO, GPION, None
    - CI-V address setting

## **rigctl Commands (Interactive Mode)**

---

### **Frequency / VFO / Split / RIT / XIT / PTT**

| Cmd   | Meaning             | Arguments     | Notes                               |
| ----- | ------------------- | ------------- | ----------------------------------- |
| **x** | Get split mode      | —             | Returns enabled/disabled            |
| **X** | Set split mode      | `<0/1> <VFO>` | Enable/disable and set split TX VFO |
| **t** | Get split frequency | —             |                                     |
| **T** | Set split frequency | `<Hz>`        |                                     |

---

### **Mode / Passband / AGC / Squelch**

| Cmd   | Meaning      | Arguments             |
| ----- | ------------ | --------------------- |
| **u** | Get passband | —                     |
| **U** | Set passband | `<Hz>`                |
| **g** | Get AGC      | —                     |
| **G** | Set AGC      | `<AGC_MODE>`          |
| **q** | Get squelch  | —                     |
| **Q** | Set squelch  | `<level>`             |

---

### **Audio: Volume / AF Gain / IF Gain / RF Gain**

| Cmd   | Meaning                    | Arguments         |                                       |
| ----- | -------------------------- | ----------------- | ------------------------------------- |
| **a** | Get antenna                | —                 |                                       |
| **A** | Set antenna                | `<ANT>`           |                                       |
| **o** | Get audio frequency (tone) | —                 |                                       |
| **O** | Set audio frequency        | `<Hz>`            |                                       |

---

### **Filters / IF / Notch / Noise Reduction / Speech Processing**

| Cmd   | Meaning              | Arguments |
| ----- | -------------------- | --------- |
| **y** | Get IF shift         | —         |
| **Y** | Set IF shift         | `<Hz>`    |
| **j** | Get noise reduction  | —         |
| **J** | Set noise reduction  | `<0/1>`   |
| **k** | Get noise blanker    | —         |
| **K** | Set noise blanker    | `<0/1>`   |
| **n** | Get notch filter     | —         |
| **N** | Set notch filter     | `<0/1>`   |
| **h** | Get speech processor | —         |
| **H** | Set speech processor | `<0/1>`   |

---

### **Rotor / Satellite / RIT/XIT Reset**

| Cmd   | Meaning                        | Arguments |
| ----- | ------------------------------ | --------- |
| **z** | Reset RIT and XIT              | —         |
| **Z** | Reset all settings to defaults | —         |

---

### **Memories / Channels**

| Cmd   | Meaning                     | Arguments   |
| ----- | --------------------------- | ----------- |
| **e** | Get memory channel          | —           |
| **E** | Set memory channel          | `<channel>` |
| **w** | Write current VFO to memory | `<channel>` |
| **W** | Read memory channel to VFO  | `<channel>` |

---

### **CTCSS / DCS / Tone Control**

| Cmd   | Meaning        | Arguments     |
| ----- | -------------- | ------------- |
| **c** | Get CTCSS tone | —             |
| **C** | Set CTCSS tone | `<tone>`      |
| **d** | Get DCS code   | —             |
| **D** | Set DCS code   | `<code>`      |
| **s** | Get tone mode  | —             |
| **S** | Set tone mode  | `<TONE_MODE>` |

---

### **Power / Attenuator / Preamp / Transceive**

| Cmd   | Meaning             | Arguments |
| ----- | ------------------- | --------- |
| **b** | Get RF power        | —         |
| **B** | Set RF power        | `<watts>` |
| **u** | Get attenuation     | —         |
| **U** | Set attenuation     | `<dB>`    |
| **k** | Get preamp          | —         |
| **K** | Set preamp          | `<0/1>`   |
| **@** | Get transceive mode | —         |
| **#** | Set transceive mode | `<0/1>`   |

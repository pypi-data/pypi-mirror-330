/**
 * Copyright 2020 The SkyWater PDK Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

`ifndef SKY130_FD_SC_HD__A2BB2OI_4_V
`define SKY130_FD_SC_HD__A2BB2OI_4_V

/**
 * a2bb2oi: 2-input AND, both inputs inverted, into first input, and
 *          2-input AND into 2nd input of 2-input NOR.
 *
 *          Y = !((!A1 & !A2) | (B1 & B2))
 *
 * Verilog top module.
 *
 * WARNING: This file is autogenerated, do not modify directly!
 */

`timescale 1ns / 1ps
`default_nettype none

`ifdef USE_POWER_PINS

`ifdef FUNCTIONAL
`include "sky130_fd_sc_hd__a2bb2oi_4.functional.pp.v"
`else  // FUNCTIONAL
`include "sky130_fd_sc_hd__a2bb2oi_4.timing.pp.v"
`endif // FUNCTIONAL

`else  // USE_POWER_PINS

`ifdef FUNCTIONAL
`include "sky130_fd_sc_hd__a2bb2oi_4.functional.v"
`else  // FUNCTIONAL
`include "sky130_fd_sc_hd__a2bb2oi_4.timing.v"
`endif // FUNCTIONAL

`endif // USE_POWER_PINS

`default_nettype wire
`endif  // SKY130_FD_SC_HD__A2BB2OI_4_V

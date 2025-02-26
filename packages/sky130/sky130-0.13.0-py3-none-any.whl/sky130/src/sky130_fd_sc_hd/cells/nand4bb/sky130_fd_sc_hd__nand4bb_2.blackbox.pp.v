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

`ifndef SKY130_FD_SC_HD__NAND4BB_2_PP_BLACKBOX_V
`define SKY130_FD_SC_HD__NAND4BB_2_PP_BLACKBOX_V

/**
 * nand4bb: 4-input NAND, first two inputs inverted.
 *
 * Verilog stub definition (black box with power pins).
 *
 * WARNING: This file is autogenerated, do not modify directly!
 */

`timescale 1ns / 1ps
`default_nettype none

(* blackbox *)
module sky130_fd_sc_hd__nand4bb_2 (
    Y   ,
    A_N ,
    B_N ,
    C   ,
    D   ,
    VPWR,
    VGND,
    VPB ,
    VNB
);

    output Y   ;
    input  A_N ;
    input  B_N ;
    input  C   ;
    input  D   ;
    input  VPWR;
    input  VGND;
    input  VPB ;
    input  VNB ;
endmodule

`default_nettype wire
`endif  // SKY130_FD_SC_HD__NAND4BB_2_PP_BLACKBOX_V

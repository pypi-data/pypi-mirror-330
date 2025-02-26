/*
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


`ifndef SKY130_FD_SC_HD__XOR3_1_TIMING_PP_V
`define SKY130_FD_SC_HD__XOR3_1_TIMING_PP_V

/**
 * xor3: 3-input exclusive OR.
 *
 *       X = A ^ B ^ C
 *
 * Verilog simulation timing model.
 */

`timescale 1ns / 1ps
`default_nettype none

// Import user defined primitives.
`include "../../models/udp_pwrgood_pp_pg/sky130_fd_sc_hd__udp_pwrgood_pp_pg.v"

`celldefine
module sky130_fd_sc_hd__xor3_1 (
    X   ,
    A   ,
    B   ,
    C   ,
    VPWR,
    VGND,
    VPB ,
    VNB
);

    // Module ports
    output X   ;
    input  A   ;
    input  B   ;
    input  C   ;
    input  VPWR;
    input  VGND;
    input  VPB ;
    input  VNB ;

    // Local signals
    wire xor0_out_X       ;
    wire pwrgood_pp0_out_X;

    //                                 Name         Output             Other arguments
    xor                                xor0        (xor0_out_X       , A, B, C               );
    sky130_fd_sc_hd__udp_pwrgood_pp$PG pwrgood_pp0 (pwrgood_pp0_out_X, xor0_out_X, VPWR, VGND);
    buf                                buf0        (X                , pwrgood_pp0_out_X     );

specify
if ((!B&!C)) (A +=> X) = (0:0:0,0:0:0);
if ((!B&C)) (A -=> X) = (0:0:0,0:0:0);
if ((B&!C)) (A -=> X) = (0:0:0,0:0:0);
if ((B&C)) (A +=> X) = (0:0:0,0:0:0);
if ((!A&!C)) (B +=> X) = (0:0:0,0:0:0);
if ((!A&C)) (B -=> X) = (0:0:0,0:0:0);
if ((A&!C)) (B -=> X) = (0:0:0,0:0:0);
if ((A&C)) (B +=> X) = (0:0:0,0:0:0);
if ((!A&!B)) (C +=> X) = (0:0:0,0:0:0);
if ((!A&B)) (C -=> X) = (0:0:0,0:0:0);
if ((A&!B)) (C -=> X) = (0:0:0,0:0:0);
if ((A&B)) (C +=> X) = (0:0:0,0:0:0);
endspecify
endmodule
`endcelldefine

`default_nettype wire
`endif  // SKY130_FD_SC_HD__XOR3_1_TIMING_PP_V

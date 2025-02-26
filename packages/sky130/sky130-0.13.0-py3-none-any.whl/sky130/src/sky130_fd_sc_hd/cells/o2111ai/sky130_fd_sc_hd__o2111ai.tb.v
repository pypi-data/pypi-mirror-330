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

`ifndef SKY130_FD_SC_HD__O2111AI_TB_V
`define SKY130_FD_SC_HD__O2111AI_TB_V

/**
 * o2111ai: 2-input OR into first input of 4-input NAND.
 *
 *          Y = !((A1 | A2) & B1 & C1 & D1)
 *
 * Autogenerated test bench.
 *
 * WARNING: This file is autogenerated, do not modify directly!
 */

`timescale 1ns / 1ps
`default_nettype none

`include "sky130_fd_sc_hd__o2111ai.v"

module top();

    // Inputs are registered
    reg A1;
    reg A2;
    reg B1;
    reg C1;
    reg D1;
    reg VPWR;
    reg VGND;
    reg VPB;
    reg VNB;

    // Outputs are wires
    wire Y;

    initial
    begin
        // Initial state is x for all inputs.
        A1   = 1'bX;
        A2   = 1'bX;
        B1   = 1'bX;
        C1   = 1'bX;
        D1   = 1'bX;
        VGND = 1'bX;
        VNB  = 1'bX;
        VPB  = 1'bX;
        VPWR = 1'bX;

        #20   A1   = 1'b0;
        #40   A2   = 1'b0;
        #60   B1   = 1'b0;
        #80   C1   = 1'b0;
        #100  D1   = 1'b0;
        #120  VGND = 1'b0;
        #140  VNB  = 1'b0;
        #160  VPB  = 1'b0;
        #180  VPWR = 1'b0;
        #200  A1   = 1'b1;
        #220  A2   = 1'b1;
        #240  B1   = 1'b1;
        #260  C1   = 1'b1;
        #280  D1   = 1'b1;
        #300  VGND = 1'b1;
        #320  VNB  = 1'b1;
        #340  VPB  = 1'b1;
        #360  VPWR = 1'b1;
        #380  A1   = 1'b0;
        #400  A2   = 1'b0;
        #420  B1   = 1'b0;
        #440  C1   = 1'b0;
        #460  D1   = 1'b0;
        #480  VGND = 1'b0;
        #500  VNB  = 1'b0;
        #520  VPB  = 1'b0;
        #540  VPWR = 1'b0;
        #560  VPWR = 1'b1;
        #580  VPB  = 1'b1;
        #600  VNB  = 1'b1;
        #620  VGND = 1'b1;
        #640  D1   = 1'b1;
        #660  C1   = 1'b1;
        #680  B1   = 1'b1;
        #700  A2   = 1'b1;
        #720  A1   = 1'b1;
        #740  VPWR = 1'bx;
        #760  VPB  = 1'bx;
        #780  VNB  = 1'bx;
        #800  VGND = 1'bx;
        #820  D1   = 1'bx;
        #840  C1   = 1'bx;
        #860  B1   = 1'bx;
        #880  A2   = 1'bx;
        #900  A1   = 1'bx;
    end

    sky130_fd_sc_hd__o2111ai dut (.A1(A1), .A2(A2), .B1(B1), .C1(C1), .D1(D1), .VPWR(VPWR), .VGND(VGND), .VPB(VPB), .VNB(VNB), .Y(Y));

endmodule

`default_nettype wire
`endif  // SKY130_FD_SC_HD__O2111AI_TB_V

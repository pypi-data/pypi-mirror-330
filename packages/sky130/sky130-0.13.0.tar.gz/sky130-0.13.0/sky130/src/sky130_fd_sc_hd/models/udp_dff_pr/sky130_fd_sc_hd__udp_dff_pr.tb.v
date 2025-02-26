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

`ifndef SKY130_FD_SC_HD__UDP_DFF_PR_TB_V
`define SKY130_FD_SC_HD__UDP_DFF_PR_TB_V

/**
 * udp_dff$PR: Positive edge triggered D flip-flop with active high
 *
 * Autogenerated test bench.
 *
 * WARNING: This file is autogenerated, do not modify directly!
 */

`timescale 1ns / 1ps
`default_nettype none

`include "sky130_fd_sc_hd__udp_dff_pr.v"

module top();

    // Inputs are registered
    reg D;
    reg RESET;

    // Outputs are wires
    wire Q;

    initial
    begin
        // Initial state is x for all inputs.
        D     = 1'bX;
        RESET = 1'bX;

        #20   D     = 1'b0;
        #40   RESET = 1'b0;
        #60   D     = 1'b1;
        #80   RESET = 1'b1;
        #100  D     = 1'b0;
        #120  RESET = 1'b0;
        #140  RESET = 1'b1;
        #160  D     = 1'b1;
        #180  RESET = 1'bx;
        #200  D     = 1'bx;
    end

    // Create a clock
    reg CLK;
    initial
    begin
        CLK = 1'b0;
    end

    always
    begin
        #5 CLK = ~CLK;
    end

    sky130_fd_sc_hd__udp_dff$PR dut (.D(D), .RESET(RESET), .Q(Q), .CLK(CLK));

endmodule

`default_nettype wire
`endif  // SKY130_FD_SC_HD__UDP_DFF_PR_TB_V

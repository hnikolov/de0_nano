//Legal Notice: (C)2016 Altera Corporation. All rights reserved.  Your
//use of Altera Corporation's design tools, logic functions and other
//software and tools, and its AMPP partner logic functions, and any
//output files any of the foregoing (including device programming or
//simulation files), and any associated documentation or information are
//expressly subject to the terms and conditions of the Altera Program
//License Subscription Agreement or other applicable license agreement,
//including, without limitation, that your use is for the sole purpose
//of programming logic devices manufactured by Altera and sold by Altera
//or its authorized distributors.  Please refer to the applicable
//agreement for further details.

// synthesis translate_off
`timescale 1ns / 1ps
// synthesis translate_on

// turn off superfluous verilog processor warnings 
// altera message_level Level1 
// altera message_off 10034 10035 10036 10037 10230 10240 10030 

module soc_system_my_onchip_memory2 (
                                      // inputs:
                                       address,
                                       byteenable,
                                       chipselect,
                                       clk,
                                       clken,
                                       reset,
                                       reset_req,
                                       write,
                                       writedata,

                                      // outputs:
                                       readdata
                                    )
;

    output  [ 31: 0] readdata;
    input   [ 13: 0] address;
    input   [  3: 0] byteenable;
    input            chipselect;
    input            clk;
    input            clken;
    input            reset;
    input            reset_req;
    input            write;
    input   [ 31: 0] writedata;
    
    wire             clocken0;
    wire    [ 31: 0] readdata;
    wire             wren;
    
    assign wren = chipselect & write;    
//  assign clocken0 = clken & ~reset_req;
  
    reg [31:0] 	 regfile [0:7];

    assign readdata = regfile[ address[3:0] ];

    always @(posedge clk) begin
        if( reset ) begin
            regfile[0] <= 32'haa_bb_cc_dd;
            regfile[1] <= 32'h11_22_33_44;
            regfile[2] <= 32'h55_66_77_88;
            regfile[3] <= 0;
            regfile[4] <= 0;
            regfile[5] <= 0;
            regfile[6] <= 0;
            regfile[7] <= 0;
        end 
        else 
        begin
            if( wren ) regfile[ address[3:0] ] <= writedata;
        end // else: !if(reset)
    end
    
    
endmodule

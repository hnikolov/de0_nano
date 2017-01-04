module sockit_test (
	//////////// CLOCK //////////
	input 		          		FPGA_CLK1_50,
	input 		          		FPGA_CLK2_50,
	input 		          		FPGA_CLK3_50,

	//////////// KEY //////////
	input 		     [1:0]		KEY,

	//////////// SW //////////
	input 		     [3:0]		SW,

	//////////// LED //////////
	output		     [7:0]		LED
);

wire [1:0] key_os;
wire [3:0] delay;
wire main_clk = FPGA_CLK1_50;

oneshot os (
    .clk       ( main_clk ),
    .edge_sig  ( KEY      ),
    .level_sig ( key_os   )
);

delay_ctrl dc (
    .reset  ( SW[3] ),
    .clk    ( main_clk  ),
    .faster ( key_os[1] ),
    .slower ( key_os[0] ),
    .delay  ( delay     )
);

blinker b (
    .reset ( SW[3]     ),
    .clk   ( main_clk  ),
    .delay ( delay     ),
    .led   ( LED       ),
    .pause ( SW[0]     )
);

endmodule

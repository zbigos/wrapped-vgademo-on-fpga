# User config
set ::env(DESIGN_NAME) "wrapped_vgademo_on_fpga"
set ::env(ROUTING_CORES) 16
set ::env(PL_RESIZER_HOLD_SLACK_MARGIN) 0.1
set ::env(GLB_RESIZER_HOLD_SLACK_MARGIN) 0.1
set ::env(TOP_MARGIN_MULT) 4
set ::env(BOTTOM_MARGIN_MULT) 4

# this might break, point it to pin_order.cfg
set ::env(FP_PIN_ORDER_CFG) $::env(DESIGN_DIR)/pin_order.cfg

set ::env(TOP_MARGIN_MULT) 4
set ::env(LEFT_MARGIN_MULT) 12
set ::env(RIGHT_MARGIN_MULT) 12

# no pins on SWE, set margins to zero.
set ::env(BOTTOM_MARGIN_MULT) 0.1

# Change if needed
set ::env(VERILOG_FILES) "$::env(DESIGN_DIR)/vgademo-on-fpga/src/*.v $::env(DESIGN_DIR)/wrapper.v"
set ::env(PL_TARGET_DENSITY) 0.60
set ::env(FP_CORE_UTIL) 50

set ::env(DESIGN_IS_CORE) 0
set ::env(RT_MAX_LAYER) {met4}

# Fill this
set ::env(CLOCK_PERIOD) "20.0"
set ::env(CLOCK_PORT) "clk"

set ::env(FP_SIZING) absolute
set ::env(DIE_AREA) "0 0 300 280"

set filename $::env(DESIGN_DIR)/$::env(PDK)_$::env(STD_CELL_LIBRARY)_config.tcl
if { [file exists $filename] == 1} {
	source $filename
}

# define power straps so the macro works inside Caravel's PDN
set ::env(VDD_NETS) [list {vccd1}]
set ::env(GND_NETS) [list {vssd1}]

# turn off CVC as we have multiple power domains
set ::env(RUN_CVC) 0

# make pins wider to solve routing issues
set ::env(FP_IO_VTHICKNESS_MULT) 4
set ::env(FP_IO_HTHICKNESS_MULT) 4

set ::env(SYNTH_DEFINES) "MPRJ_IO_PADS=38"
set ::env(PL_RESIZER_BUFFER_OUTPUT_PORTS) 0

set ::env(DIODE_INSERTION_STRATEGY) 3
set ::env(GLB_RT_MAX_DIODE_INS_ITERS) 10
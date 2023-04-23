include <../../solid2/extensions/bosl2/BOSL2/version.scad>;
include <../../solid2/extensions/bosl2/BOSL2/constants.scad>;
include <../../solid2/extensions/bosl2/BOSL2/transforms.scad>;
include <../../solid2/extensions/bosl2/BOSL2/distributors.scad>;
include <../../solid2/extensions/bosl2/BOSL2/mutators.scad>;
include <../../solid2/extensions/bosl2/BOSL2/color.scad>;
include <../../solid2/extensions/bosl2/BOSL2/attachments.scad>;
include <../../solid2/extensions/bosl2/BOSL2/shapes3d.scad>;
include <../../solid2/extensions/bosl2/BOSL2/shapes2d.scad>;
include <../../solid2/extensions/bosl2/BOSL2/drawing.scad>;
include <../../solid2/extensions/bosl2/BOSL2/masks3d.scad>;
include <../../solid2/extensions/bosl2/BOSL2/masks2d.scad>;
include <../../solid2/extensions/bosl2/BOSL2/math.scad>;
include <../../solid2/extensions/bosl2/BOSL2/paths.scad>;
include <../../solid2/extensions/bosl2/BOSL2/lists.scad>;
include <../../solid2/extensions/bosl2/BOSL2/comparisons.scad>;
include <../../solid2/extensions/bosl2/BOSL2/linalg.scad>;
include <../../solid2/extensions/bosl2/BOSL2/trigonometry.scad>;
include <../../solid2/extensions/bosl2/BOSL2/vectors.scad>;
include <../../solid2/extensions/bosl2/BOSL2/affine.scad>;
include <../../solid2/extensions/bosl2/BOSL2/coords.scad>;
include <../../solid2/extensions/bosl2/BOSL2/geometry.scad>;
include <../../solid2/extensions/bosl2/BOSL2/regions.scad>;
include <../../solid2/extensions/bosl2/BOSL2/strings.scad>;
include <../../solid2/extensions/bosl2/BOSL2/skin.scad>;
include <../../solid2/extensions/bosl2/BOSL2/vnf.scad>;
include <../../solid2/extensions/bosl2/BOSL2/utility.scad>;
include <../../solid2/extensions/bosl2/BOSL2/partitions.scad>;





difference() {
	union() {
		tube(or = 30.3577490736, center = true, h = 88, ir = 28.3577490736);
		down(z = 40) {
			zcyl(h = 10, r = 35.5577490736);
		}
	}
	union() {
		cylindrical_extrude(or = 30.5577490736, ir = 30.3577490736) {
			offset(r = 0.0000000000) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 30.3577490736, ir = 30.1577490736) {
			offset(r = -0.0123116594) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 30.1577490736, ir = 29.9577490736) {
			offset(r = -0.0489434837) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 29.9577490736, ir = 29.7577490736) {
			offset(r = -0.1089934758) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 29.7577490736, ir = 29.5577490736) {
			offset(r = -0.1909830056) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 29.5577490736, ir = 29.3577490736) {
			offset(r = -0.2928932188) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 29.3577490736, ir = 29.1577490736) {
			offset(r = -0.4122147477) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 29.1577490736, ir = 28.9577490736) {
			offset(r = -0.5460095003) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 28.9577490736, ir = 28.7577490736) {
			offset(r = -0.6909830056) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		cylindrical_extrude(or = 28.7577490736, ir = 28.5577490736) {
			offset(r = -0.8435655350) {
				projection(cut = true) {
					translate(v = [0, 0, 10]) {
						surface(center = true, file = "maze7.png", invert = true);
					}
				}
			}
		}
		zrot(a = 120.0000000000) {
			union() {
				cylindrical_extrude(or = 30.5577490736, ir = 30.3577490736) {
					offset(r = 0.0000000000) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 30.3577490736, ir = 30.1577490736) {
					offset(r = -0.0123116594) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 30.1577490736, ir = 29.9577490736) {
					offset(r = -0.0489434837) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.9577490736, ir = 29.7577490736) {
					offset(r = -0.1089934758) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.7577490736, ir = 29.5577490736) {
					offset(r = -0.1909830056) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.5577490736, ir = 29.3577490736) {
					offset(r = -0.2928932188) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.3577490736, ir = 29.1577490736) {
					offset(r = -0.4122147477) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.1577490736, ir = 28.9577490736) {
					offset(r = -0.5460095003) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 28.9577490736, ir = 28.7577490736) {
					offset(r = -0.6909830056) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 28.7577490736, ir = 28.5577490736) {
					offset(r = -0.8435655350) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
			}
		}
		zrot(a = 240.0000000000) {
			union() {
				cylindrical_extrude(or = 30.5577490736, ir = 30.3577490736) {
					offset(r = 0.0000000000) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 30.3577490736, ir = 30.1577490736) {
					offset(r = -0.0123116594) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 30.1577490736, ir = 29.9577490736) {
					offset(r = -0.0489434837) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.9577490736, ir = 29.7577490736) {
					offset(r = -0.1089934758) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.7577490736, ir = 29.5577490736) {
					offset(r = -0.1909830056) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.5577490736, ir = 29.3577490736) {
					offset(r = -0.2928932188) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.3577490736, ir = 29.1577490736) {
					offset(r = -0.4122147477) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 29.1577490736, ir = 28.9577490736) {
					offset(r = -0.5460095003) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 28.9577490736, ir = 28.7577490736) {
					offset(r = -0.6909830056) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
				cylindrical_extrude(or = 28.7577490736, ir = 28.5577490736) {
					offset(r = -0.8435655350) {
						projection(cut = true) {
							translate(v = [0, 0, 10]) {
								surface(center = true, file = "maze7.png", invert = true);
							}
						}
					}
				}
			}
		}
	}
}

OPENQASM 2.0;
include "qelib1.inc";
qreg q[10];
h q[0];
h q[1];
cx q[0],q[1];
rz(0.22733602246716966) q[1];
cx q[0],q[1];
h q[0];
ry(0.31675833970975287) q[0];
h q[0];
h q[1];
ry(0.7973654573327341) q[1];
h q[1];
h q[2];
h q[3];
cx q[2],q[3];
rz(0.6762546707509746) q[3];
cx q[2],q[3];
h q[2];
ry(0.391109550601909) q[2];
h q[2];
cx q[1],q[2];
rz(0.8864799193275177) q[2];
cx q[1],q[2];
h q[1];
ry(0.6974534998820221) q[1];
h q[2];
ry(0.3264728640701121) q[2];
h q[2];
cx q[0],q[2];
rz(0.12946907617720027) q[2];
cx q[0],q[2];
h q[0];
ry(0.09166475154493592) q[0];
h q[0];
h q[2];
ry(0.5985680136649132) q[2];
h q[2];
h q[3];
ry(0.33281392786638453) q[3];
h q[3];
h q[4];
h q[5];
cx q[4],q[5];
rz(0.5983087535871898) q[5];
cx q[4],q[5];
h q[4];
ry(0.18673418560371335) q[4];
h q[4];
cx q[3],q[4];
rz(0.7339281633300665) q[4];
cx q[3],q[4];
h q[3];
ry(0.22013495554548623) q[3];
h q[4];
ry(0.08159456954220812) q[4];
h q[4];
h q[5];
ry(0.6727560440146213) q[5];
h q[5];
h q[6];
h q[7];
cx q[6],q[7];
rz(0.9418028652699372) q[7];
cx q[6],q[7];
h q[6];
ry(0.248245714629571) q[6];
h q[6];
cx q[5],q[6];
rz(0.15989560107504752) q[6];
cx q[5],q[6];
h q[5];
ry(0.3401001849547053) q[5];
h q[6];
ry(0.46519315370205094) q[6];
h q[6];
cx q[4],q[6];
rz(0.8547419043740013) q[6];
cx q[4],q[6];
h q[4];
ry(0.6016212416937131) q[4];
h q[4];
cx q[2],q[4];
rz(0.7247813610920201) q[4];
cx q[2],q[4];
h q[2];
ry(0.8605513173932924) q[2];
h q[4];
ry(0.9293378015753163) q[4];
h q[4];
cx q[0],q[4];
rz(0.2737731824899875) q[4];
cx q[0],q[4];
h q[0];
ry(0.4517787074747607) q[0];
h q[0];
h q[4];
ry(0.6650389233995303) q[4];
h q[4];
h q[6];
ry(0.9319883611359835) q[6];
h q[6];
h q[7];
ry(0.9488811518333182) q[7];
h q[7];
h q[8];
h q[9];
cx q[8],q[9];
rz(0.6672374531003724) q[9];
cx q[8],q[9];
h q[8];
ry(0.09589793559411208) q[8];
h q[8];
cx q[7],q[8];
rz(0.26642102829077097) q[8];
cx q[7],q[8];
h q[7];
ry(0.815776403424807) q[7];
h q[8];
ry(0.1932943892894945) q[8];
h q[8];
cx q[6],q[8];
rz(0.546186009082353) q[8];
cx q[6],q[8];
h q[6];
ry(0.9376729587677569) q[6];
h q[8];
ry(0.4949879400788243) q[8];
h q[8];
cx q[4],q[8];
rz(0.33089093046705464) q[8];
cx q[4],q[8];
h q[4];
ry(0.9034540068082391) q[4];
h q[8];
ry(0.2570741752765343) q[8];
h q[8];
cx q[0],q[8];
rz(0.33982833761031983) q[8];
cx q[0],q[8];
h q[0];
ry(0.25885339864292733) q[0];
h q[8];
ry(0.355446479944286) q[8];
h q[9];
ry(0.4418396661678128) q[9];
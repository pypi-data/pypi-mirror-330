# PYTHONVENV="/path/to/python/env" bash test_pipeline.sh

SCRIPTDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd; );
PAWPYRUS=$( realpath "${SCRIPTDIR}/../src/pawpyrus/main.py"; ); 
if [[ "$2" = "package" ]];
then {
	echo "PACKAGE!";
	EXEC="pawpyrus";
} else {
	EXEC="python3 ${PAWPYRUS}";
} fi
TESTDIR="${SCRIPTDIR}/test";
DEBUGDIR="${TESTDIR}/debug";
TESTIMAGES="${TESTDIR}/images";
TESTIMAGESFN="${TESTIMAGES}/page";
TESTOUTPUT="${TESTDIR}/test.pdf";
TESTFILE="${SCRIPTDIR}/birthday-cake.png";
TESTOUTFILE="${TESTDIR}/birthday-cake.png";
PAWPYRUS=$( realpath "${SCRIPTDIR}/../src/pawpyrus/main.py"; );
RESOLUTION=300;

rm -rf "${TESTDIR}"
mkdir "${TESTDIR}"
${EXEC} Encode -n "Test Job" -i "${TESTFILE}" -o "${TESTOUTPUT}"
mkdir "${TESTIMAGES}"
pdftoppm -progress -png -rx "${RESOLUTION}" -ry "${RESOLUTION}" "${TESTOUTPUT}" "${TESTIMAGESFN}"
${EXEC} Decode -i "${TESTIMAGES}/*" -o "${TESTOUTFILE}" -d "${DEBUGDIR}"
${EXEC} Decode -t "${DEBUGDIR}/blocks.txt" -o "${TESTOUTFILE}"

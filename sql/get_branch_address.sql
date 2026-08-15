
CREATE OR REPLACE FUNCTION get_branch_address (
    p_branchno IN dh_branch.branchno%TYPE
)
RETURN VARCHAR2
IS
    v_address VARCHAR2(200);
BEGIN
    SELECT street || ', ' || city
    INTO v_address
    FROM dh_branch
    WHERE branchno = p_branchno;

    RETURN v_address;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN 'Branch not found';
END get_branch_address;
/


SET SERVEROUTPUT ON;
BEGIN
    DBMS_OUTPUT.PUT_LINE(get_branch_address('B002'));
END;
/


SELECT get_branch_address('B002') AS branch_address FROM dual;

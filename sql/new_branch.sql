

CREATE OR REPLACE PROCEDURE new_branch (
    p_branchno  IN dh_branch.branchno%TYPE,
    p_street    IN dh_branch.street%TYPE,
    p_city      IN dh_branch.city%TYPE,
    p_postcode  IN dh_branch.postcode%TYPE
)
IS
BEGIN

    INSERT INTO dh_branch (branchno, street, city, postcode)
    VALUES (p_branchno, p_street, p_city, p_postcode);

    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END new_branch;
/


BEGIN
    new_branch(
        p_branchno => 'B099',
        p_street   => '35 Raven Street',
        p_city     => 'London',
        p_postcode => 'NW1 6XE'
    );
END;
/

SELECT * FROM dh_branch WHERE branchno = 'B099';

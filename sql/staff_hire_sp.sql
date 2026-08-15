
CREATE OR REPLACE PROCEDURE staff_hire_sp (
    p_staffno     IN dh_staff.staffno%TYPE,
    p_fname       IN dh_staff.fname%TYPE,
    p_lname       IN dh_staff.lname%TYPE,
    p_position    IN dh_staff.position%TYPE,
    p_sex         IN dh_staff.sex%TYPE,
    p_dob         IN dh_staff.dob%TYPE,
    p_salary      IN dh_staff.salary%TYPE,
    p_branchno    IN dh_staff.branchno%TYPE,
    p_telephone   IN dh_staff.telephone%TYPE
)
IS
BEGIN
    INSERT INTO dh_staff (
        staffno, fname, lname, position, sex, dob, salary, branchno, telephone
    ) VALUES (
        p_staffno, p_fname, p_lname, p_position, p_sex, p_dob, p_salary, p_branchno, p_telephone
    );

    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;  
END staff_hire_sp;
/


BEGIN
    staff_hire_sp(
        p_staffno  => 'SG99',
        p_fname    => 'Test',
        p_lname    => 'User',
        p_position => 'Assistant',
        p_sex      => 'F',
        p_dob      => TO_DATE('1995-05-01', 'YYYY-MM-DD'),
        p_salary   => 30000,
        p_branchno  => 'B002',
        p_telephone => '555-1234'
    );
END;
/

-- Confirm it worked:
SELECT * FROM dh_staff WHERE staffno = 'SG99';
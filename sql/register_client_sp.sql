

CREATE OR REPLACE PROCEDURE register_client_sp (
    p_clientno   IN dh_client.clientno%TYPE,
    p_fname      IN dh_client.fname%TYPE,
    p_lname      IN dh_client.lname%TYPE,
    p_telno      IN dh_client.telno%TYPE,
    p_street     IN dh_client.street%TYPE,
    p_city       IN dh_client.city%TYPE,
    p_email      IN dh_client.email%TYPE,
    p_preftype   IN dh_client.preftype%TYPE,
    p_maxrent    IN dh_client.maxrent%TYPE
)
IS
BEGIN
    INSERT INTO dh_client (
        clientno, fname, lname, telno, street, city, email, preftype, maxrent
    ) VALUES (
        p_clientno, p_fname, p_lname, p_telno, p_street, p_city, p_email, p_preftype, p_maxrent
    );

    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END register_client_sp;
/

BEGIN
    register_client_sp(
        p_clientno => 'CL99',
        p_fname    => 'Test',
        p_lname    => 'Client',
        p_telno    => '555-9999',
        p_street   => '10 Main St',
        p_city     => 'Toronto',
        p_email    => 'test@example.com',
        p_preftype => 'Flat',
        p_maxrent  => 1200
    );
END;
/

SELECT * FROM dh_client WHERE clientno = 'CL99';

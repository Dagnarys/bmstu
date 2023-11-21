DROP TABLE insurance CASCADE;
DROP TABLE driver_insurance CASCADE;
DROP TABLE driver CASCADE;
DROP TABLE users CASCADE;

--Создание таблицы Водитель
CREATE TABLE driver (
    id serial PRIMARY KEY,
    full_name VARCHAR NOT NULL,
    birth_date DATE NOT NULL,
    address VARCHAR,
    phone_number VARCHAR,
    email VARCHAR,
    driver_license_number VARCHAR NOT NULL,
    issue_date DATE, -- дата выдачи ву
    expiration_date DATE, -- срок действия
    passport_number VARCHAR, -- номер паспорта
    status BOOLEAN,
    url_photo VARCHAR NULL
);
--Создание таблицы Страховка
CREATE TABLE insurance (
    id serial PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    premium_amount FLOAT NOT NULL,
    insurance_type BOOLEAN,
    id_user INT NOT NULL,
    id_moderator INT NOT NULL,
    status VARCHAR,
    --Статус заявки:
    --Создана
    --Обработана
    --Отказана
    --Оформлена
    --Удалена
    date_create DATE,
    date_form DATE,
    date_over DATE,
    vehicle_make VARCHAR, --марка
    vehicle_model VARCHAR, -- модель
    vehicle_year VARCHAR, --год выпуска
    vehicle_vin VARCHAR(17),
    vehicle_license_plate VARCHAR(10) -- гос.номер.
);
--Создание таблицы Пользователь
CREATE TABLE users (
    id serial PRIMARY KEY,
    login VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    admin BOOLEAN NOT NULL
);
--Создание таблицы СтраховкиВодители
CREATE TABLE driver_insurance(
    id serial PRIMARY KEY,
    id_driver INT NOT NULL,
    id_insurance INT NOT NULL

);
--связывание таблицы СтраховкиВодители
alter table driver_insurance
add constraint FR_driver_insurance_of_driver
    foreign key (id_driver) references driver(id);

alter table driver_insurance
add constraint FR_driver_insurance_of_insurance
    foreign key (id_insurance) references insurance(id);
--связывание таблицы Страховка с пользователем
ALTER TABLE insurance
ADD CONSTRAINT FR_insurance_of_user
    FOREIGN KEY (id_user) REFERENCES users (id);
--связывание таблицы Страховка с модератором
ALTER TABLE insurance
ADD CONSTRAINT FR_insurance_of_moderator
    FOREIGN KEY (id_moderator) REFERENCES users (id);




--удаление таблиц



--вставка пользователей
INSERT INTO users (login, password, admin)
VALUES
       ('user1','user1',false),
       ('user2','user2',false),
       ('user3','user3',false),
       ('user4','user4',false),
       ('admin','admin',true);

select * from users;

--вставка водителей
INSERT INTO driver (full_name, birth_date, address,
                    phone_number, email, driver_license_number,
                    issue_date, expiration_date, passport_number,
                    status,url_photo)
VALUES
        ('Козлова Елена Михайловна', '1992-04-03', 'ул. Морская, д. 78, кв. 22', '+7 (555) 789-1234', 'elena@example.com', 'GH567890', '2017-09-18', '2027-09-18', '2345 678901', true,'/imgs/img1.png'),
        ('Иванов Иван Иванович', '1980-05-15', 'ул. Примерная, д. 123, кв. 45', '+7 (123) 456-7890', 'ivan@example.com', 'AB123456', '2005-07-20', '2030-07-20', '1234 567890', true,'/imgs/img2.png'),
        ('Петрова Петра Петровна', '1995-02-28', 'ул. Образцовая, д. 45, кв. 12', '+7 (987) 654-3210', 'petra@example.com', 'CD789012', '2018-11-10', '2028-11-10', '5678 901234', true, '/imgs/img3.png'),
        ('Сидоров Алексей Васильевич', '1988-08-10', 'пр. Приморский, д. 56, кв. 3', '+7 (777) 123-4567', 'alex@example.com', 'EF345678', '2010-03-05', '2030-03-05', '9012 345678', true,'/imgs/img4.png'),
        ('Григорьев Дмитрий Николаевич', '1975-12-20', 'пр. Ленина, д. 34, кв. 7', '+7 (111) 987-6543', 'dmitry@example.com', 'IJ123456', '2002-06-12', '2032-06-12', '6789 012345', true,'/imgs/img5.png');

select * from driver;

--вставка страховок
--Статус заявки:
    --Создана
    --Обработана
    --Отказана
    --Оформлена
    --Удалена
INSERT INTO insurance (start_date, end_date, premium_amount,
                       insurance_type, id_user, id_moderator,
                       status, date_create, date_form, date_over,
                       vehicle_make, vehicle_model, vehicle_year,
                       vehicle_vin, vehicle_license_plate)
VALUES
('2023-01-01', '2023-12-31', 5000.00, true, 1, 5, 'Создана', '2023-01-05', '2023-01-10', '2023-12-31', 'Toyota', 'Camry', '2019', 'ABC12345678901234', 'А123ВС01'),
('2023-02-15', '2023-08-14', 4000.50, true, 2, 5, 'Обработана', '2023-02-20', '2023-02-25', '2023-08-14', 'Honda', 'Civic', '2021', 'XYZ98765432109876', 'В234АВ02'),
('2023-03-10', '2023-09-09', 3500.75, false, 3, 5, 'Отказана', '2023-03-15', '2023-03-20', '2023-09-09', 'Ford', 'Focus', '2020', 'MNO45678901234567', 'Е567ЕЕ03'),
('2023-04-20', '2023-10-19', 4500.25, false, 4, 5, 'Оформлена', '2023-04-25', '2023-04-30', '2023-10-19', 'Chevrolet', 'Cruze', '2018', 'PQR12345678901234', 'К789АК04'),
('2023-05-05', '2023-11-04', 6000.00, true, 5, 5, 'Удалена', '2023-05-10', '2023-05-15', '2023-11-04', 'Nissan', 'Altima', '2017', 'STU98765432109876', 'Л123МЛ05');

SELECT * FROM insurance;

--вставка водителей_страховок
INSERT INTO driver_insurance (id_driver, id_insurance)
VALUES
(1,1),
(1,2),
(2,3),
(3,4),
(4,1);

SELECT * FROM driver_insurance;

SELECT
    d.full_name AS driver_name,
    i.vehicle_make AS vehicle_make,
    i.vehicle_model AS vehicle_model,
    i.start_date AS insurance_start_date,
    i.end_date AS insurance_end_date
FROM
    driver AS d
INNER JOIN
    driver_insurance AS di ON d.id = di.id_driver
INNER JOIN
    insurance AS i ON di.id_insurance = i.id;
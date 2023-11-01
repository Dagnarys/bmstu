import psycopg2

from prettytable import PrettyTable


class Database():

    # создание связи с бд
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host='127.0.0.1',
                user='postgres',
                password='postgres',
                database='postgres',
                port=5432,
            )
            print("sucessful connection db")
        except Exception as ex:
            print("Error connection", ex)

    # удаление таблиц
    def drop_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                DROP TABLE insurance CASCADE;
                DROP TABLE driver_insurance CASCADE;
                DROP TABLE driver CASCADE;
                DROP TABLE users CASCADE;
                """)
                self.connection.commit()
                print("succesful delete tables")
        except Exception as ex:
            print("Error w/ PostgreSQL ", ex)

    def create_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
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
                    """)
                self.connection.commit()
                print("Успешно созданы таблицы в БД")

        except Exception as ex:
            print("Ошибка при работе с PostgreSQL:", ex)

    # Заполнение записи в таблицу в БД
    def insert_default_value(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
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
--вставка пользователей
                    INSERT INTO users (login, password, admin)
                    VALUES
                           ('user1','user1',false),
                           ('user2','user2',false),
                           ('user3','user3',false),
                           ('user4','user4',false),
                           ('admin','admin',true);
    
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



                            --вставка водителей_страховок
                            INSERT INTO driver_insurance (id_driver, id_insurance)
                            VALUES
                            (1,1),
                            (1,2),
                            (2,1),
                            (3,1),
                            (4,1);

                            
                            

                    
                    
                    
                    """)
                # Подтверждение изменений
                self.connection.commit()
                print(" Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print(" Ошибка при заполнение данных:", ex)

    def insert_driver(self, full_name, birth_date, address, phone_number, email,
                      driver_license_number, issue_date, expiration_date,
                      passport_number, status, url_photo):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO driver (full_name, birth_date, address, 
                phone_number, email, driver_license_number, issue_date, 
                expiration_date, passport_number, status, url_photo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (full_name, birth_date, address,
                      phone_number, email, driver_license_number, issue_date,
                      expiration_date, passport_number, status, url_photo)
                               )
                self.connection.commit()
                print("driver succesful added")
        except Exception as ex:
            self.connection.rollback()
            print("driver didn't add", ex)

    def insert_insurance(self, start_date, end_date, premium_amount,
                         insurance_type, id_user, id_moderator,
                         status, date_create, date_form, date_over,
                         vehicle_make, vehicle_model, vehicle_year,
                         vehicle_vin, vehicle_license_plate):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO driver (start_date, end_date, premium_amount,
                       insurance_type, id_user, id_moderator,
                       status, date_create, date_form, date_over,
                       vehicle_make, vehicle_model, vehicle_year,
                       vehicle_vin, vehicle_license_plate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (start_date, end_date, premium_amount,
                      insurance_type, id_user, id_moderator,
                      status, date_create, date_form, date_over,
                      vehicle_make, vehicle_model, vehicle_year,
                      vehicle_vin, vehicle_license_plate)
                               )
                self.connection.commit()
                print("insurance succesful added")
        except Exception as ex:
            self.connection.rollback()
            print("insurance didn't add", ex)

    def insert_driver_insurance(self, id_driver, id_insurance):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                INSERT INTO driver (id_driver, id_insurance)
                VALUES (%s, %s,);
                """, (id_driver, id_insurance)
                               )
                self.connection.commit()
                print("driver_insurance succesful added")
        except Exception as ex:
            self.connection.rollback()
            print("driver_insurance didn't add", ex)

    # Выводит все записи
    def select_all(self):
        try:
            with self.connection.cursor() as cursor:
                database = {}
                name_table = ['users', 'driver', 'insurance', 'driver_insurance']
                database['name_table'] = name_table
                for name in name_table:
                    cursor.execute(f"""SELECT * FROM {name};""")
                    database[name] = cursor.fetchall()
                    # Получим названия колонок из cursor.description
                    database[f'{name}_name_col'] = [col[0] for col in cursor.description]

                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("Ошибка при чтении данных:", ex)

    def print_select_all(self, database):
        data_print = []

        for name in database['name_table']:
            table = PrettyTable()
            table.field_names = database[f'{name}_name_col']
            for row in database[name]:
                table.add_row(row)
            # Выводим таблицу на консоль
            # print(table)
            data_print.append(table)

        return data_print

    # Обновление статуса в таблице Водитель
    def update_status_delete_driver(self, status, id_driver):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE driver SET status = %s WHERE id = %s;""",
                    (status, id_driver)
                )
                # Подтверждение изменений
                self.connection.commit()
                print("[Status] Данные успешно обновлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[Status] Ошибка при обновление данных:", ex)

    # Выводит записи в таблицу Водитель в котором статус доступен
    def get_driver_with_status_true(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM driver as D
                        WHERE D.status = true;
                    """)
                # Получаем данные
                results = cursor.fetchall()
                # Подтверждение изменений
                self.connection.commit()
                print("Driver Данные успешно прочитаны")

                database = []
                for obj in results:
                    data = {
                        'id': obj[0],
                        'full_name': obj[1],
                        'birth_date': obj[2],
                        'address': obj[3],
                        'phone_number': obj[4],
                        'email': obj[5],
                        'driver_license_number': obj[6],
                        'issue_date': obj[7],
                        'expiration_date': obj[8],
                        'passport_number': obj[9],
                        'status': obj[10],
                        'url_photo': obj[11],

                    }
                    database.append(data)
                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("Driver Ошибка при чтение данных:", ex)

        # Выводит записи таблицы Driver

    def get_driver_for_id(self, id_driver):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """SELECT * FROM driver as D
                        WHERE D.id = %s;
                    """, (id_driver,)
                )
                # Получаем данные
                results = cursor.fetchall()
                # Подтверждение изменений
                self.connection.commit()
                print("Driver Данные успешно прочитаны")

                database = []
                for obj in results:
                    data = {
                        'id': obj[0],
                        'full_name': obj[1],
                        'birth_date': obj[2],
                        'address': obj[3],
                        'phone_number': obj[4],
                        'email': obj[5],
                        'driver_license_number': obj[6],
                        'issue_date': obj[7],
                        'expiration_date': obj[8],
                        'passport_number': obj[9],
                        'status': obj[10],
                        'url_photo': obj[11],
                    }
                    database.append(data)
                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("Driver Ошибка при чтение данных:", ex)

    def get_driver_insurance_by_id(self, id_driver):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """SELECT
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
                    """, (id_driver,)
                )
                # Получаем данные
                results = cursor.fetchall()
                # Подтверждение изменений
                self.connection.commit()
                print("driver_insurance Данные успешно прочитаны")

                database = []
                for obj in results:
                    data = {
                        'd_full_namde': obj[0],
                        'i_vehicle_make': obj[1],
                        'i_vehicle_model': obj[2],
                        'i_start_date': obj[3],
                        'i_end_date': obj[4],
                    }
                    database.append(data)

                return database
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("driver_insurance Ошибка при чтение данных:", ex)

    def close(self):
        # Закрытие соединения
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")


# Вызов функции
db = Database()
# Вызов функции для подключения к БД
db.connect()
db.drop_table()

# Вызов функции для создания таблицы в БД
db.create_table()

# Вызов функции для заполнения записей в таблицу БД
db.insert_default_value()

# Вызов функции для добавления новых записей города
# db.insert_driver()
# Вызов функции для добавления новых записей вакансий
# db.insert_insurance()
# Вызов функции для добавления новых записей вакансиигорода
# # db.insert_driver_insurance()

# Вызов функции для вывода все записи
# db.select_all()
# Вызов функции печать для вывода все записи
# db.print_select_all()

# Вызов функции для обновления статуса в таблице Город
# db.update_status_delete_city(True, 5)

# Вызов функции для вывода записей из разных таблиц в одну таблицу
# db.get_vacancycity()
# db.get_vacancycity_by_id(1)

# Вызов функции для вывода записи в таблицу Город в котором статус доступен
# db.get_city_with_status_true()

# Вызов функции для закрытия БД
# db.close()
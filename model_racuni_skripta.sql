-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb3 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`racuni`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`racuni` (
  `broj_racuna` INT NOT NULL,
  `datum_izdavanja` DATE NOT NULL,
  `zaduzeno_lice` VARCHAR(45) NOT NULL,
  `status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`broj_racuna`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`sektor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`sektor` (
  `identifikacioni_broj` INT NOT NULL,
  `naziv_sektora` VARCHAR(45) NOT NULL,
  `racuni_broj_racuna` INT NOT NULL,
  PRIMARY KEY (`identifikacioni_broj`, `racuni_broj_racuna`),
  INDEX `fk_sektor_racuni1_idx` (`racuni_broj_racuna` ASC) VISIBLE,
  CONSTRAINT `fk_sektor_racuni1`
    FOREIGN KEY (`racuni_broj_racuna`)
    REFERENCES `mydb`.`racuni` (`broj_racuna`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`korisnik`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`korisnik` (
  `JMBG` INT NOT NULL,
  `Ime` VARCHAR(45) NOT NULL,
  `Prezime` VARCHAR(45) NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(85) NOT NULL,
  `sektor` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(45) NULL DEFAULT NULL,
  `sektor_identifikacioni_broj` INT NOT NULL,
  `racuni_broj_racuna` INT NOT NULL,
  PRIMARY KEY (`JMBG`, `sektor_identifikacioni_broj`, `racuni_broj_racuna`),
  INDEX `fk_korisnik_sektor_idx` (`sektor_identifikacioni_broj` ASC) VISIBLE,
  INDEX `fk_korisnik_racuni1_idx` (`racuni_broj_racuna` ASC) VISIBLE,
  CONSTRAINT `fk_korisnik_sektor`
    FOREIGN KEY (`sektor_identifikacioni_broj`)
    REFERENCES `mydb`.`sektor` (`identifikacioni_broj`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_korisnik_racuni1`
    FOREIGN KEY (`racuni_broj_racuna`)
    REFERENCES `mydb`.`racuni` (`broj_racuna`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

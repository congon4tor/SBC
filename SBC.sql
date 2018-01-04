-- phpMyAdmin SQL Dump
-- version 4.7.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jan 04, 2018 at 03:14 PM
-- Server version: 10.1.29-MariaDB
-- PHP Version: 7.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `SBC`
--

-- --------------------------------------------------------

--
-- Table structure for table `ASISTENTE`
--

CREATE TABLE `ASISTENTE` (
  `ID_Asistente` int(11) NOT NULL,
  `DNI` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `TAG` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Apellidos` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Nivel_Acceso` int(1) NOT NULL DEFAULT '0',
  `Creditos` int(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ASISTENTE_SALA`
--

CREATE TABLE `ASISTENTE_SALA` (
  `ID_Asistente` int(11) NOT NULL,
  `ID_Sala` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `HISTORIAL`
--

CREATE TABLE `HISTORIAL` (
  `ID_Asistente` int(11) NOT NULL,
  `ID_Sala` int(11) NOT NULL,
  `Hora_Entrada` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Hora_Salida` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `HISTORIAL_CREDITOS`
--

CREATE TABLE `HISTORIAL_CREDITOS` (
  `ID_Asistente` int(11) NOT NULL,
  `creditos` int(11) NOT NULL,
  `modo_pago` tinyint(1) NOT NULL,
  `hora` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `SALA`
--

CREATE TABLE `SALA` (
  `ID_Sala` int(11) NOT NULL,
  `Nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Nivel_Acceso` int(1) NOT NULL DEFAULT '0',
  `Aforo_Act` int(11) NOT NULL,
  `Aforo_Max` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ASISTENTE`
--
ALTER TABLE `ASISTENTE`
  ADD PRIMARY KEY (`ID_Asistente`),
  ADD UNIQUE KEY `DNI` (`DNI`),
  ADD UNIQUE KEY `TAG` (`TAG`);

--
-- Indexes for table `ASISTENTE_SALA`
--
ALTER TABLE `ASISTENTE_SALA`
  ADD UNIQUE KEY `ID_Asistente` (`ID_Asistente`),
  ADD KEY `ID_Sala` (`ID_Sala`);

--
-- Indexes for table `HISTORIAL`
--
ALTER TABLE `HISTORIAL`
  ADD KEY `ID_Asistente` (`ID_Asistente`),
  ADD KEY `ID_Sala` (`ID_Sala`);

--
-- Indexes for table `HISTORIAL_CREDITOS`
--
ALTER TABLE `HISTORIAL_CREDITOS`
  ADD KEY `ID_Asistente` (`ID_Asistente`);

--
-- Indexes for table `SALA`
--
ALTER TABLE `SALA`
  ADD PRIMARY KEY (`ID_Sala`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ASISTENTE`
--
ALTER TABLE `ASISTENTE`
  MODIFY `ID_Asistente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `SALA`
--
ALTER TABLE `SALA`
  MODIFY `ID_Sala` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ASISTENTE_SALA`
--
ALTER TABLE `ASISTENTE_SALA`
  ADD CONSTRAINT `ASISTENTE_SALA_ibfk_1` FOREIGN KEY (`ID_Asistente`) REFERENCES `ASISTENTE` (`ID_Asistente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ASISTENTE_SALA_ibfk_2` FOREIGN KEY (`ID_Sala`) REFERENCES `SALA` (`ID_Sala`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `HISTORIAL`
--
ALTER TABLE `HISTORIAL`
  ADD CONSTRAINT `HISTORIAL_ibfk_1` FOREIGN KEY (`ID_Asistente`) REFERENCES `ASISTENTE` (`ID_Asistente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `HISTORIAL_ibfk_2` FOREIGN KEY (`ID_Sala`) REFERENCES `SALA` (`ID_Sala`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `HISTORIAL_CREDITOS`
--
ALTER TABLE `HISTORIAL_CREDITOS`
  ADD CONSTRAINT `HISTORIAL_CREDITOS_ibfk_1` FOREIGN KEY (`ID_Asistente`) REFERENCES `ASISTENTE` (`ID_Asistente`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

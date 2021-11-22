-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: August 11, 2020 at 02:21 PM
-- Server version: 5.7.29-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `REAL_ESTATE_VN`
--

-- --------------------------------------------------------

DROP TABLE IF EXISTS `MUABANNHADAT`;

--
-- Table structure for table `MOGIVN`
--

CREATE TABLE `MUABANNHADAT` (
  `ID_CLIENT` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `SITE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `ADS_LINK` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `FOR_SALE` int(11) DEFAULT '0',
  `FOR_LEASE` int(11) DEFAULT '0',
  `TO_BUY` int(11) DEFAULT '0',
  `TO_LEASE` int(11) DEFAULT '0',
  `LAND_TYPE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `ADS_DATE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PRICE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PRICE_UNIT` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PRICE_M2` double DEFAULT '0',
  `SURFACE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `SURFACE_UNIT` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `USED_SURFACE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `USED_SURFACE_UNIT` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PRO_WIDTH` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PRO_LENGTH` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `LEGAL_STATUS` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PRO_CURRENT_STATUS` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PRO_DIRECTION` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `FRONTAGE` float DEFAULT '0',
  `ALLEY_ACCESS` float DEFAULT '0',
  `NB_LOTS` int(11) DEFAULT '0',
  `PRO_UTILITIES` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `NB_ROOMS` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `NB_FLOORS` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `KITCHEN` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `BEDROOM` int(11) DEFAULT '0',
  `BATHROOM` int(11) DEFAULT '0',
  `GARAGE` int(11) DEFAULT '0',
  `TOILET` int(11) DEFAULT '0',
  `FULL_ADDRESS` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `STREET` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `WARD` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DISTRICT` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `CITY` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `LAT` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `LON` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PHOTOS` int(11) DEFAULT NULL,
  `ADS_TITLE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `BRIEF` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DETAILED_BRIEF` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DEALER_ID` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DEALER_NAME` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DEALER_TYPE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DEALER_ADDRESS` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DEALER_EMAIL` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DEALER_TEL` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `DEALER_JOIN_DATE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `PROJECT_NAME` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `AGENCY_NAME` mediumtext COLLATE utf8mb4_bin,
  `AGENCY_ADDRESS` mediumtext COLLATE utf8mb4_bin,
  `AGENCY_CITY` mediumtext COLLATE utf8mb4_bin,
  `AGENCY_TEL` mediumtext COLLATE utf8mb4_bin,
  `AGENCY_WEBSITE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `MINI_SITE` mediumtext CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `RESTAURANT` int(11) DEFAULT '0',
  `BANK` int(11) DEFAULT '0',
  `COFFEESHOP` int(11) DEFAULT '0',
  `PARK` int(11) DEFAULT '0',
  `STADIUM` int(11) DEFAULT '0',
  `SHOPPING` int(11) DEFAULT '0',
  `SUPERMARKET` int(11) DEFAULT '0',
  `GYM` int(11) DEFAULT '0',
  `SCHOOL` int(11) DEFAULT '0',
  `CINEMA` int(11) DEFAULT '0',
  `HOSPITAL` int(11) DEFAULT '0',
  `AIRPORT` int(11) DEFAULT '0',
  `ZOO` int(11) DEFAULT '0',
  `ANIMAL_STORE` int(11) DEFAULT '0',
  `CLOTH_STORE` int(11) DEFAULT '0',
  `SPA` int(11) DEFAULT '0',
  `PARKING` int(11) DEFAULT '0',
  `NIGHT_CLUB` int(11) DEFAULT '0',
  `ENTERTAINMENT_PARK` int(11) DEFAULT '0',
  `BAKERY_STORE` int(11) DEFAULT '0',
  `GROCERIES` int(11) DEFAULT '0',
  `POST_OFFICE` int(11) DEFAULT '0',
  `ATM` int(11) DEFAULT '0',
  `BAR` int(11) DEFAULT '0',
  `CHECK_CONVERT` int(11) DEFAULT '0',
  `PRO_FLAG` int(5) DEFAULT '0',
  `CREATED_DATE` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `MOGIVN`
--
ALTER TABLE `MUABANNHADAT`
  ADD PRIMARY KEY (`ID_CLIENT`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

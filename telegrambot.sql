-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 10, 2020 at 09:18 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `telegrambot`
--

-- --------------------------------------------------------

--
-- Table structure for table `adcampaign`
--

CREATE TABLE `adcampaign` (
  `campaignId` int(11) NOT NULL,
  `title` varchar(128) NOT NULL,
  `description` text NOT NULL,
  `nsfw` tinyint(1) NOT NULL,
  `clicks` int(11) NOT NULL,
  `cpc` float NOT NULL,
  `dailyBudget` float NOT NULL,
  `status` tinyint(1) NOT NULL,
  `url` varchar(512) NOT NULL,
  `userId` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `balance`
--

CREATE TABLE `balance` (
  `address` varchar(64) NOT NULL,
  `history` varchar(64) NOT NULL,
  `balance` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sees`
--

CREATE TABLE `sees` (
  `userId` varchar(64) NOT NULL,
  `campaignId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userId` varchar(64) NOT NULL,
  `referral` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  `taskAlert` tinyint(1) NOT NULL,
  `seeNsfw` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adcampaign`
--
ALTER TABLE `adcampaign`
  ADD PRIMARY KEY (`campaignId`),
  ADD KEY `userId` (`userId`);

--
-- Indexes for table `balance`
--
ALTER TABLE `balance`
  ADD PRIMARY KEY (`address`);

--
-- Indexes for table `sees`
--
ALTER TABLE `sees`
  ADD KEY `campaignId` (`campaignId`),
  ADD KEY `userId` (`userId`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`userId`),
  ADD KEY `address` (`address`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `adcampaign`
--
ALTER TABLE `adcampaign`
  ADD CONSTRAINT `adcampaign_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`);

--
-- Constraints for table `sees`
--
ALTER TABLE `sees`
  ADD CONSTRAINT `sees_ibfk_1` FOREIGN KEY (`campaignId`) REFERENCES `adcampaign` (`campaignId`),
  ADD CONSTRAINT `sees_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `user` (`userId`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`address`) REFERENCES `balance` (`address`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

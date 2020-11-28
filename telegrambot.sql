-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 28, 2020 at 11:15 PM
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
  `username` varchar(128) NOT NULL,
  `country` varchar(5) DEFAULT NULL,
  `totalclicks` int(11) NOT NULL,
  `seconds` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adcampaign`
--

INSERT INTO `adcampaign` (`campaignId`, `title`, `description`, `nsfw`, `clicks`, `cpc`, `dailyBudget`, `status`, `url`, `username`, `country`, `totalclicks`, `seconds`) VALUES
(56, 'provatitolo1', 'provadescrizione1', 0, 0, 0.029, 72, 1, 'http://prova1.com', 'IonutZuZu', 'xx', 0, 0),
(57, 'wwwwwww', 'ssssssssssssssssss', 0, 0, 0.0292, 292, 1, 'http://fffffffffff', 'IonutZuZu', 'xx', 0, 10),
(58, 'wwwwwwww', 'wwwwwwwwwwww', 0, 0, 0.0291, 1456, 1, 'http://fffffffffffssssss', 'IonutZuZu', 'xx', 0, 10),
(59, 'aaaaaaa', 'aaaaaaaaaaaaaaaa', 1, 0, 0.0291, 1456, 1, 'http://aaaaaaaaaaaa', 'IonutZuZu', 'xx', 0, 10),
(60, 'titolo2', 'description2', 1, 0, 0.0292, 292, 1, 'https://addddd2', 'IonutZuZu', 'xx', 0, 10),
(61, 'titolo3', 'description3', 1, 0, 0.0292, 1462, 1, 'http://titolo3', 'IonutZuZu', 'xx', 0, 10),
(62, 'rrrrrrr', 'ttttttttt', 1, 1, 1, 22, 1, 'wewewwew', 'wwwwwww', 'ww', 1, 12),
(63, 'titolo4', 'desssscription4', 1, 0, 0.0292, 1463, 1, 'http://titolo4', 'IonutZuZu', 'xx', 0, 10),
(64, 'eeeeeeeeee', 'rrrrrrrrrrrrrrrrrr', 1, 0, 0.0294, 73, 1, 'http://www.ggggg.pc', 'IonutZuZu', 'xx', 0, 10),
(65, 'wwwwww', 'eeeeeeeeeee', 1, 0, 0.443, 2956, 1, 'http://wwwwwww.com', 'IonutZuZu', 'xx', 0, 10),
(66, 'wwwwwww', 'eeeeeeeeee', 0, 0, 0.148, 1480, 1, 'http://ssssss.com', 'IonutZuZu', 'xx', 0, 10);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `userId` varchar(64) NOT NULL,
  `referral` varchar(64) NOT NULL,
  `taskAlert` tinyint(1) NOT NULL,
  `seeNsfw` tinyint(1) NOT NULL,
  `address` varchar(64) NOT NULL,
  `referredBy` varchar(64) NOT NULL,
  `country` varchar(5) DEFAULT NULL,
  `username` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userId`, `referral`, `taskAlert`, `seeNsfw`, `address`, `referredBy`, `country`, `username`) VALUES
('626602519', 'bPEKnEKO', 1, 1, '2N5ApERYxn2mWiK584KEb3Y6qZtX9n8YHKp', '', 'en', 'IonutZuZu'),
('666666', 'eeeeee', 1, 1, 'wwwwwwwww', 'wwwwwwwww', 'ww', 'wwwwwww');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adcampaign`
--
ALTER TABLE `adcampaign`
  ADD PRIMARY KEY (`campaignId`),
  ADD KEY `username` (`username`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`) USING BTREE,
  ADD UNIQUE KEY `address` (`address`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adcampaign`
--
ALTER TABLE `adcampaign`
  MODIFY `campaignId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `adcampaign`
--
ALTER TABLE `adcampaign`
  ADD CONSTRAINT `adcampaign_ibfk_2` FOREIGN KEY (`username`) REFERENCES `user` (`username`),
  ADD CONSTRAINT `adcampaign_ibfk_3` FOREIGN KEY (`username`) REFERENCES `user` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

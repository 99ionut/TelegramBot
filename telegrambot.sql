-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 05, 2020 at 11:29 PM
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
  `country` varchar(100) DEFAULT NULL,
  `totalclicks` int(11) NOT NULL,
  `seconds` int(11) NOT NULL,
  `dateAdded` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adcampaign`
--

INSERT INTO `adcampaign` (`campaignId`, `title`, `description`, `nsfw`, `clicks`, `cpc`, `dailyBudget`, `status`, `url`, `username`, `country`, `totalclicks`, `seconds`, `dateAdded`) VALUES
(56, 'provatitolo1', 'provadescrizione1', 0, 0, 0.029, 72, 1, 'http://prova1.com', 'IonutZuZu', 'xx', 0, 0, NULL),
(67, 'lllllll', 'kkkkkkkkkkkkkk', 0, 0, 0.1419, 283, 1, 'http://sssssss.com', 'IonutZuZu', 'xx', 0, 10, NULL),
(68, 'èèèèèèèèèèèè', 'ooooooooooooooo', 1, 0, 0.148, 296, 1, 'http://ooooooo.com', 'IonutZuZu', 'xx', 0, 10, '0000-00-00'),
(69, 'tttttttttttttttt', 'rrrrrrrrrrrrrrrr', 1, 0, 0.148, 592, 1, 'http://ttttttttttttttt.com', 'IonutZuZu', 'xx', 0, 10, '2020-11-10'),
(70, 'eeeeeeeeeeee', 'rrrrrrrrrrrrrrrrrrrrrr', 1, 0, 0.1478, 295, 1, 'http://wwwwwwwwww.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-05'),
(71, 'gggggggggggggg', 'ggggggggggggggggggg', 1, 0, 0.0295, 0, 1, 'http://nnnnnnnnnnnnnnnn.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-05'),
(72, 'wwwwwwwwwwww', 'wwwwwwwwwwwwwwww', 1, 0, 0.0296, 0, 1, 'http://wwwwwwwwwwww.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-05'),
(73, 'pppppppppppp', 'ooooooooooooo', 1, 0, 0.1475, 73, 1, 'http://ssssssss.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-05'),
(74, 'rrrrrrrrrr', 'tttttttttttttt', 0, 0, 0.148, 74, 1, 'http://wwwwwwwwwwww.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-05'),
(75, 'pppppppppppp', 'oooooooooooooooo', 0, 0, 0.04, 73, 1, 'http://ssssssssssss.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-05'),
(76, 'pppppppppppp', 'wwwwwwwwww', 0, 0, 0.09, 34, 1, 'http://sssssssssss.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-05'),
(77, '3333333333333', '44444444444444', 0, 0, 0.1479, 999, 1, 'http://poooooooooooooo.com', 'IonutZuZu', 'xx', 0, 10, '2020-12-05'),
(78, 'oooooooooooo', 'ppppppppppp', 1, 0, 0.0293, 293, 1, 'http://sssssssss.com', 'IonutZuZu', 'us,de,gb,fr,', 0, 10, '2020-12-05'),
(79, 'ppppppppp', 'ooooooooooo', 1, 0, 0.1467, 2934, 1, 'http://sssssssssssssss.com', 'IonutZuZu', 'ng,de,vn,nl,ph,in,ve,gb,', 0, 10, '2020-12-05');

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
  `username` varchar(128) NOT NULL,
  `dateJoined` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`userId`, `referral`, `taskAlert`, `seeNsfw`, `address`, `referredBy`, `country`, `username`, `dateJoined`) VALUES
('626602519', 'bPEKnEKO', 1, 0, '2N5ApERYxn2mWiK584KEb3Y6qZtX9n8YHKp', '', 'en', 'IonutZuZu', NULL),
('374408239', 'LdWxuVuw', 1, 1, '2My1b62H5U4uQiYZvd8nXDt1rxdcQUnzGre', '', 'de', 'Trafficbossadmin', NULL),
('666666', 'eeeeee', 1, 1, 'wwwwwwwww', 'wwwwwwwww', 'ww', 'wwwwwww', NULL);

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
  MODIFY `campaignId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=80;

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

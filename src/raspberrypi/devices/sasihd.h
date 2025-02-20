//---------------------------------------------------------------------------
//
//	SCSI Target Emulator RaSCSI (*^..^*)
//	for Raspberry Pi
//
//	Copyright (C) 2001-2006 ＰＩ．(ytanaka@ipc-tokai.or.jp)
//	Copyright (C) 2014-2020 GIMONS
//  	Copyright (C) akuker
//
//  	Licensed under the BSD 3-Clause License. 
//  	See LICENSE file in the project root folder.
//
//  [ SASI hard disk ]
//
//---------------------------------------------------------------------------
#pragma once

#include "os.h"
#include "disk.h"
#include "filepath.h"

//===========================================================================
//
//	SASI Hard Disk
//
//===========================================================================
class SASIHD : public Disk, public FileSupport
{
public:
	SASIHD(const unordered_set<uint32_t>&);
	~SASIHD() {}

	void Reset();
	void Open(const Filepath&) override;

	vector<BYTE> RequestSense(int) override;
	vector<BYTE> Inquiry() const override;
	virtual void ReadCapacity10(SASIDEV *) override;
};
